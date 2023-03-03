########################

import time
import logging
import argsparser
from flask_restx import *
from flask import *

########################

print('loading model')

from transformers import AutoModelForCausalLM, AutoTokenizer
import textwrap, time

MAX_NEW_TOKENS = 300
model_name = "acul3/bloomz-3b-Instruction"

model = AutoModelForCausalLM.from_pretrained(
  model_name,
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

###

def prompt_to_resoonse(
	prompt,
	max_length,
	):
	input_ids = tokenizer(prompt, return_tensors="pt").input_ids
	generated_ids = model.generate(
		input_ids, 
		max_length=max_length, 
		pad_token_id=tokenizer.eos_token_id, 
		do_sample=True, 
		top_p=0.95, 
		temperature=0.5, 
		penalty_alpha=0.6, 
		top_k=4, 
		repetition_penalty=1.03, 
		num_return_sequences=1)
	result = textwrap.wrap(tokenizer.decode(generated_ids[0], skip_special_tokens=True), width=128)
	result[0] = result[0].split("Asisten:")[-1]
	return "\n".join(result)

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