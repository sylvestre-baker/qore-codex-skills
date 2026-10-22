// Offline first-party reproduction. No server, dependency loading, or credentials.
// Run: node review/verifier-reproduction.mjs [absolute-target-directory]
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';

const target = process.argv[2] || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../target');
const pins = {
  'src/modules/common/utils/response.ts':'ecc4ba57cbcf7b3492fb17f280feb8f0d9a8a60773a4519788ea6ae36e399645',
  'src/modules/interfaces/api/i.model.response.ts':'0054263a1d94ef0d9b71ea31a1377a04245a4002df60bc1cef0c5bf18a2e1554',
  'src/modules/database/services/service.mongo.db.client.ts':'700fc925abf4b5b59e8dd815c09e8d0fe5f8c74c992f8101cf0b3a5a93cf22f0',
  'src/modules/users/services/stores/store.user.ts':'f85773b76b346ae632bd3f85267cd5ebc87c5cf907e87af3f4efac79248d3b46',
  'src/modules/users/services/service.user.ts':'5caf315031c19aa7fbb95e5af9eef839245a9febc93349ecace956da0f88d507',
  'src/servers/sample.typescrit.swagger.api/controllers/controller.user.ts':'0698ebf32b2b20d2e791d3652ec2616fdc18bd535a9de9989caa1f62cd45920e',
  'src/modules/users/models/user.ts':'4232d5c32eac1ff8cb2f886b51a9b1ed605afdb85258eca7f9f7bfa35d94d504'
};
// Validate every file before any extracted code is evaluated.
for (const [file, expected] of Object.entries(pins)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(target,file))).digest('hex'), expected, 'Target source hash mismatch: '+file);
}
const records = [];
function slice(relative, start, end) {
  const bytes = fs.readFileSync(path.join(target, relative));
  const text = bytes.toString().split('\n').slice(start - 1, end).join('\n');
  records.push({file: relative, lines: [start, end], file_sha256: crypto.createHash('sha256').update(bytes).digest('hex'), span_sha256: crypto.createHash('sha256').update(text).digest('hex')});
  return text;
}
// Only isolated named method spans are evaluated; constructors/config are never loaded.
const response = slice('src/modules/common/utils/response.ts', 52, 58)
  .replace('export function ResponseFailure(code: number, message: string)', 'function ResponseFailure(code, message)');
const model = slice('src/modules/interfaces/api/i.model.response.ts', 1, 6);
assert.match(model, /message: string;/);
assert.doesNotMatch(model, /constructor|toJSON|=/);
class IModelResponse {}
const dictionarySource = slice('src/modules/common/utils/response.ts', 3, 31)
  .replace('const dictCodeHttpResponse: { [id: number]: string }', 'const dictCodeHttpResponse');
const dictionary = new Function(dictionarySource + '\nreturn dictCodeHttpResponse;')();
const ResponseFailure = new Function('IModelResponse', 'dictCodeHttpResponse', response + '\nreturn ResponseFailure;')(IModelResponse, dictionary);
const dbSource = slice('src/modules/database/services/service.mongo.db.client.ts', 42, 46)
  .replace('public findOneById(collection: string, objectId: string, result: (error, data) => void): void', 'findOneById(collection, objectId, result)');
const dbMethod = new Function('ObjectID', 'return ({' + dbSource + '}).findOneById;')(class ObjectID {constructor(id) {this.id = id;}});
const getSource = slice('src/modules/users/services/stores/store.user.ts', 50, 59)
  .replace('get(id: string): Promise<ModelUser>', 'get(id)')
  .replace('new Promise<ModelUser>', 'new Promise')
  .replace('(error, data: ModelUser)', '(error, data)');
const get = new Function('return ({' + getSource + '}).get;')();
const serviceSource = slice('src/modules/users/services/service.user.ts', 81, 98)
  .replace('async find(findUser: FindUserByIdRequest): Promise<IModelResponse>', 'async find(findUser)');
const find = new Function('ResponseFailure', 'ResponseSuccess', 'return ({' + serviceSource + '}).find;')(ResponseFailure, () => {throw new Error('Unexpected success');});
const controllerSource = slice('src/servers/sample.typescrit.swagger.api/controllers/controller.user.ts', 47, 67)
  .replace('public async find(req: Request, res: Response)', 'async find(req, res)');
const controllerFind = new Function('appInsights','jwt','config','ResponseFailure', 'return ({' + controllerSource + '}).find;')({defaultClient:{trackNodeHttpRequest(){}, trackException(){}}}, {verify(){return {userId:'offline-id'};}}, {secret:'offline-placeholder'}, ResponseFailure);
const contract = slice('src/modules/users/models/user.ts', 27, 48);
assert.match(contract, /name: "UserErrorResponse"/);
assert.match(contract, /message: string;/);
const annotation = slice('src/servers/sample.typescrit.swagger.api/controllers/controller.user.ts', 29, 46);
assert.match(annotation, /500: \{ model: "UserErrorResponse" \}/);

const observations = [];
for (const [name, failure] of [['native_Error',new Error('offline database failure')], ['string_control','public safe message']]) {
  const mongoClient = {findOneById:dbMethod, db:{collection(){return {findOne(_query, callback){callback(failure, null);}};}}};
  const store = {get, mongoClient, collectionName:'offline-users'};
  const service = {find, store};
  let sent, status;
  const res = {status(value){status=value;return this;},send(value){sent=value;return this;}};
  await controllerFind.call({serviceUser:service}, {headers:{authorization:'Bearer offline-placeholder'},body:{userId:'offline-id'}}, res);
  assert.equal(status, 500);
  assert.equal(sent.message, failure);
  // Explicit ECMAScript serialization experiment, NOT an Express implementation.
  const json = JSON.stringify(sent);
  const parsed = JSON.parse(json);
  assert.deepEqual(Object.keys(parsed), ['code','error','message']);
  observations.push({case:name,captured_status:status,same_error_identity:sent.message===failure,captured_fields:Object.keys(sent),json_experiment:json,json_fields:Object.keys(parsed),message_json_type:typeof parsed.message,conforms_to_declared_message_string:typeof parsed.message==='string'});
}
assert.equal(observations[0].conforms_to_declared_message_string,false);
assert.equal(observations[1].conforms_to_declared_message_string,true);
console.log(JSON.stringify({node:process.version,source_records:records,assumptions:['TypeScript type annotations and declared-only fields are erased; only shown method signatures and type arguments removed.','Mongo callback failure is injected; real MongoDB behavior was not exercised.','ObjectID, JWT authorization and telemetry are offline stubs. Authenticated matching-user branch is exercised.','Response mock captures send argument only. JSON.stringify is a separate experiment, not proof of actual Express bytes.','No installed Express/Swagger/Joi implementation or generated consumer exists in the supplied target.'],observations},null,2));
