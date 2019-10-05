import requests,hmac, hashlib, base64, json, re
from datetime import datetime

class UnleashedBase:
	"""
		Base class for making a connection to API of unleashedsoftware.com
		Inputs:
			auth_id : Your user account Authorization ID assigned by Unleashed
			auth_sig: Your user account Authorization signature assigned by Unleashed
			api_add: the address of the api access to Unleashed, typically https://api.unleashedsoftware.com
	"""

	def __init__(self, auth_id, auth_sig,  api_add):
		self.header = {'Content-Type': 'application/json', \
			'Accept':'application/json',\
			'api-auth-id':auth_id,
			'api-auth-signature':None}
		self.auth_sig = auth_sig
		self.auth_id = auth_id
		self.api_add = api_add

	@staticmethod
	def getSignature(args, privateKey):
		# print(args)
		key = str.encode(privateKey, encoding='ASCII')
		msg = str.encode(args, encoding='ASCII')
		myhmacsha256 = hmac.new(key, msg, digestmod=hashlib.sha256).digest()
		return base64.b64encode(myhmacsha256).decode()

class Resource(UnleashedBase):

	def __init__(self, resource_name, auth_id, auth_sig,  api_add, **kwargs):
		super().__init__(auth_id, auth_sig,  api_add)
		# Create the filter:
		self.resource_name = resource_name
		self.filter = ''
		for name, value in kwargs.items():
			if self.filter == '':
			# print('{0}={1}'.format(name, value))
				self.filter += '{0}={1}'.format(name, value)
			else:
				self.filter += '&{0}={1}'.format(name, value)
		# print(self.filter)
		if self.filter is not None:
			self.header['api-auth-signature'] = self.getSignature(self.filter,self.auth_sig)
			self.address = self.api_add+'/'+self.resource_name+'?'+self.filter
		else:
			self.header['api-auth-signature'] = self.getSignature('',self.auth_sig)
			self.header = self.header
			self.address = self.api_add+'/'+self.resource_name

	def first_page(self):
		"""
			Given a product object, this method will return the first page
			of paginated results that Unleashed gives back with the git request

			Returns:
				json object containing results from first page of git request
		"""
		# print(self.address, self.header)
		return(json.dumps(requests.get(self.address, headers = self.header).json()['Items']))

	def all_results(self):
		pages = self.getPages()
		results = []
		for i in range(1,pages + 1):
			r = requests.get(self.address, headers = self.header).json()['Items']
			for result in r:
				results.append(result)
		return(json.dumps(results))

	def getPages(self):

		return(requests.get(self.address, headers = self.header).json()['Pagination']['NumberOfPages'])

class EditableResource(Resource):

	def __init__(self, resource_name, auth_id, auth_sig,  api_add, **kwargs):
		super().__init__(resource_name, auth_id, auth_sig,  api_add, **kwargs)

	def post_object(self, guid, object):
		"""
			submit object to unleashed.
		"""
		return(requests.post(self.address, headers = self.header, data = object))
