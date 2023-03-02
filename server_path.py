########################

import time
import logging
import argsparser
from flask_restx import *
from flask import *

########################

print('loading model')


'''
from transformers import pipeline, set_seed

set_seed(42)

model_id = "bigscience/bloomz-7b1"

pipe = pipeline(
	model = model_id, 
	)

'''

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


from transformers import pipeline, set_seed
from transformers import AutoModelForCausalLM, AutoTokenizer

'''

set_seed(42)

###

model_id = "bigscience/bloomz-7b1"

###

model = AutoModelForCausalLM.from_pretrained(
	model_id,
	)

tokenizer = AutoTokenizer.from_pretrained(
	model_id,
	)

###

def prompt_to_resoonse(
	prompt,
	max_length,
	):
	inputs = tokenizer(
		prompt, 
		return_tensors="pt",
		)
	model_output = model.generate(
		**inputs,
		output_scores=True,
		max_length = max_length,
		)
	response = tokenizer.batch_decode(
		model_output, 
		skip_special_tokens=True)[0]
	return response

'''

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

parser_bloomz_7b1 = ns.parser()
parser_bloomz_7b1.add_argument('prompt', type=str, location='json')
parser_bloomz_7b1.add_argument('max_length', type=int, location='json')

bloomz_7b1_api_req = ns.model(
	'bloomz_7b1', 
	{
	'prompt': fields.String(example = "My name is Jimmy. Question: what is my name?"),
	'max_length': fields.Integer(example = 128),
	})

@ns.route('/bloomz_7b1')
class bloomz_7b1_api(Resource):
	def __init__(self, *args, **kwargs):
		super(bloomz_7b1_api, self).__init__(*args, **kwargs)
	@ns.expect(bloomz_7b1_api_req)
	def post(self):		
		start = time.time()
		try:			
			args = parser_bloomz_7b1.parse_args()

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