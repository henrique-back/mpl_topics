import get_data.helper as helper

config = helper.read_config()

api_key = config['SCOPUSSettings']['api_key']
insttoken = config['SCOPUSSettings']['insttoken']

print("\nDisplaying FTP details\n")

print("SCOPUS API_Key: " + api_key)
print("SCOPUS Insttoken: " + insttoken)