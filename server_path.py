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

model_id = "EleutherAI/gpt-neo-1.3B"

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

'''
prompt_to_resoonse(
	"My name is Jimmy. Question: what is my name?",
	max_length = 128,
	)
'''

print('model loaded.')

########################

args = argsparser.prepare_args()

######

ns = Namespace(
	'large_language_model', 
	)

########################################################

parser_gpt_neo_1b = ns.parser()
parser_gpt_neo_1b.add_argument('prompt', type=str, location='json')
parser_gpt_neo_1b.add_argument('max_length', type=int, location='json')

gpt_neo_1b_api_req = ns.model(
	'gpt_neo_1b', 
	{
	'prompt': fields.String(example = "My name is Jimmy. Question: what is my name?"),
	'max_length': fields.Integer(example = 128),
	})

@ns.route('/gpt_neo_1b')
class gpt_neo_1b_api(Resource):
	def __init__(self, *args, **kwargs):
		super(gpt_neo_1b_api, self).__init__(*args, **kwargs)
	@ns.expect(gpt_neo_1b_api_req)
	def post(self):		
		start = time.time()
		try:			
			args = parser_gpt_neo_1b.parse_args()

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