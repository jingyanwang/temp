########################

import time
import logging
import argsparser
from flask_restx import *
from flask import *

########################

print('loading model')

set_seed(42)

###

from transformers import pipeline

model_id = "facebook/opt-iml-max-1.3b"

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
prompt = u"""
input: I live in Miami.
output: Miami

input: I live in Houston.
output: Houston

input: I live in New York.
output: 
"""

prompt_to_resoonse(
	prompt,
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

parser_opt_iml_max_1b = ns.parser()
parser_opt_iml_max_1b.add_argument('prompt', type=str, location='json')
parser_opt_iml_max_1b.add_argument('max_length', type=int, location='json')

opt_iml_max_1b_api_req = ns.model(
	'opt_iml_max_1b', 
	{
	'prompt': fields.String(example = "My name is Jimmy. Question: what is my name?"),
	'max_length': fields.Integer(example = 128),
	})

@ns.route('/opt_iml_max_1b')
class opt_iml_max_1b_api(Resource):
	def __init__(self, *args, **kwargs):
		super(opt_iml_max_1b_api, self).__init__(*args, **kwargs)
	@ns.expect(opt_iml_max_1b_api_req)
	def post(self):		
		start = time.time()
		try:			
			args = parser_opt_iml_max_1b.parse_args()

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