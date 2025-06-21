## Create bearer token
1- Open Home Assistant then open User profile
2 Go to the bottom then click on create token to generate token

Example of generated token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJiOWE1NTg1OWM1MTg0ZDEzOGRhYjhkY2VkM2ZhZTdjNSIsImlhdCI6MTY4NzQ0ODU0MywiZXhwIjoyMDAyODA4NTQzfQ.WOyWjyeyLSMBtWlMeoapOjXDPfBsOI4yBvN2TEDoLNU

## API Smoke test
1- Open postman
2- Import RASPBERRY_HOME_ASSISTANT.postman_environment.json
3- Import Raspberry-Home-Assistant.postman_collection.json
4- Edit Environment RASPBERRY_HOME_ASSISTANT and update HASSIO_URL with the current IP of the Raspberry Pi
5- Edit Environment ACCESS_TOKEN with generated token from Home Assistant
5- Open raspberry hassio api endpoint
6- Open Authorization section and verify Bearer token is being selected from dropbox and {{ACCESS_TOKEN}} is set on Token Texbox
8- Send request

Expected result 
{
    "message": "API running."
}

For further information visit https://developers.home-assistant.io/docs/api/rest/


# Turn on and Turn off Smoke Test
1- Open raspberry hassio api services climate turn on
2- Open Authorization section and verify Bearer token is being selected from dropbox and {{ACCESS_TOKEN}} is set on Token Texbox
3- Open Body section and verify entity id json property matches with entity id of smart climate integration widget from home assistant