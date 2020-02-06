# Gallery

A simple Django application that provides APIs to upload, list, publish and delete photos

A sample is hosted at http://jibinjohnkj.pythonanywhere.com/

## APIs

- Post a photo 
	- POST /api/photos/
	- data = {  
					"caption":  "A beautiful sea",  
					"media":  file, 
					"user":  2,  
					"published_on":  "1999-01-01T01:01:00Z" 
					}
- Save photos as draft - as above, without a published_on
- Edit photo captions
	- PATCH /api/photos/1
	- data = {
      "caption": "A wonderful tree",
	  }
- Delete photos - DELETE /api/photos/1
	
- List photos 
  - all - GET /api/photos/
  - my photos - GET /api/photos/?user_id=1
  - my drafts - GET /api/photos/?draft=true
- Sort photos on publishing date
  - ASC - GET api/photos/
  - DESC - GET  api/photos/?sort=-published_on
- Filter photos by user - /api/photos/?user_id=1
- JWT authentication
	 -  get token 
	      - POST /api-token-auth/
	      - data = {
            "username": username,
            "password": password,
            }
	  - authentication
	      - Use header "Authorization: JWT \<token>"
