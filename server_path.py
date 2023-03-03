########################

import time
import logging
import argsparser
from flask_restx import *
from flask import *

########################

print('loading model')


from transformers import pipeline, set_seed

set_seed(42)

model_id = "acul3/bloomz-3b-Instruction"

pipe = pipeline(
	model = model_id, 
	)

###

def prompt_to_resoonse(
	prompt,
	max_length,
	):
	response = pipe(
		prompt,
		return_full_text = False,
		max_length = max_length,
	)
	return response[0]['generated_text']

print('model loaded.')

########################

args = argsparser.prepare_args()

######

ns = Namespace(
	'large_language_model', 
	)

########################################################

parser_bloomz_3b_instruction = ns.parser()
parser_bloomz_3b_instruction.add_argument('prompt', type=str, location='json')
parser_bloomz_3b_instruction.add_argument('max_length', type=int, location='json')

bloomz_3b_instruction_api_req = ns.model(
	'bloomz_3b_instruction', 
	{
	'prompt': fields.String(example = "My name is Jimmy. Question: what is my name?"),
	'max_length': fields.Integer(example = 128),
	})

@ns.route('/bloomz_3b_instruction')
class bloomz_3b_instruction_api(Resource):
	def __init__(self, *args, **kwargs):
		super(bloomz_3b_instruction_api, self).__init__(*args, **kwargs)
	@ns.expect(bloomz_3b_instruction_api_req)
	def post(self):		
		start = time.time()
		try:			
			args = parser_bloomz_3b_instruction.parse_args()

			output = {}

			output['response'] = prompt_to_resoonse(
				prompt = args['prompt'],
				max_length = args['max_length'],
				)

			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output = {}
			output['status'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output

########################################################