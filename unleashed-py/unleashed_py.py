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
		"""
			Takes in all the arguments for filtering the results of an api requests
			and builds the api authorization signature that needs to be send in the header with any requestself.

			Input:
				args: the entire string to be used as a filter of results
				privateKey: The unleashed designated authorization signature unique to each user.
			Returns:
				A decoded hash string suitable for Unleashed to read.
		"""
		key = str.encode(privateKey, encoding='ASCII')
		msg = str.encode(args, encoding='ASCII')
		myhmacsha256 = hmac.new(key, msg, digestmod=hashlib.sha256).digest()
		return base64.b64encode(myhmacsha256).decode()

class Resource(UnleashedBase):
	"""
		Class for getting information out of the Unleashed API.
		All Unleashed Software resources can be read using this class.
		For full list of available resources and corresponding filters see: https://apidocs.unleashedsoftware.com

		Input:
			resource_name: any of the availabe Unleashed Resources
			auth_id : Your user account Authorization ID assigned by Unleashed
			auth_sig: Your user account Authorization signature assigned by Unleashed
			api_add: the address of the api access to Unleashed, typically https://api.unleashedsoftware.com
			**kwargs: Any of the filters availbe for each Unleashed API resource as key-value pairs e.g. productCode='Artifact'
	"""

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
			Given a resource object, this method will return the first page
			of paginated results that Unleashed gives back with the get request

			Returns:
				json object containing results from first page of get request
		"""
		# print(self.address, self.header)
		return(json.dumps(requests.get(self.address, headers = self.header).json()['Items']))

	def all_results(self):
		"""
			For any resource return the entire list of those resources in your Unleashed database.

			Returns:
				json object containing every result from get request
		"""
		pages = self.getPages()
		results = []
		for i in range(1,pages + 1):
			r = requests.get(self.address, headers = self.header).json()['Items']
			for result in r:
				results.append(result)
		return(json.dumps(results))

	def getPages(self):
		"""
			Method to return the number of pages of information a resouce request has.
		"""
		return(requests.get(self.address, headers = self.header).json()['Pagination']['NumberOfPages'])

class EditableResource(Resource):
	"""
		Class for getting and posting information out of the Unleashed API.
		All Unleashed Software resources can be read using this class, and the editable resources can be posted back to the system.
		For full list of available resources and corresponding filters see: https://apidocs.unleashedsoftware.com

		Input:
			resource_name: any of the availabe Unleashed Resources
			auth_id : Your user account Authorization ID assigned by Unleashed
			auth_sig: Your user account Authorization signature assigned by Unleashed
			api_add: the address of the api access to Unleashed, typically https://api.unleashedsoftware.com
			**kwargs: Any of the filters availbe for each Unleashed API resource as key-value pairs e.g. productCode='Artifact'
	"""

	def __init__(self, resource_name, auth_id, auth_sig,  api_add, **kwargs):
		super().__init__(resource_name, auth_id, auth_sig,  api_add, **kwargs)

	def post_object(self, guid, object):
		"""
			For an editable resource post that resource to the Unleashed api

			Inputs:
				guid: New or existing GUID representing the object to be posted.
				object: JSON object to be posted to unleashed.
		"""
		return(requests.post(self.address, headers = self.header, data = object))
