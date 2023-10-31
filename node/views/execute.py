from uc_flow_nodes.views import execute
from uc_http_requester.requester import Request
from uc_flow_schemas.flow import RunState
from uc_flow_nodes.schemas import NodeRunContext
from node.schemas.enums import NodeAction
from node.views.utils import generate_jwt, get_request_body

URL_AUTH = 'https://accounts.google.com/o/oauth2/token'
URL_UPLOAD = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart'
URL_LIST = 'https://www.googleapis.com/drive/v3/files/'

class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            node_action = json.node.data.properties['node_action']

            # Авторизация
            if node_action == NodeAction.auth:
                file_info = json.node.data.properties['file_info']
                private_key = json.node.data.properties['private_key']
                jwt_token = generate_jwt(private_key)

                auth_data = {
                    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                    'assertion': jwt_token
                    }
                
                url = URL_AUTH

                headers = {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                        }

                auth_request = Request(
                    url=url,
                    method=Request.Method.post,
                    json=auth_data,
                    headers=headers)
            
                auth_result = await auth_request.execute()
                auth_result_data = auth_result.json()
                
                access_token = auth_result_data['access_token']

                await json.save_result({
                    "access_token": access_token,
                    "file_info": file_info,
                    })
                json.state = RunState.complete
            
            # Загрузка файла
            if node_action == NodeAction.upload_file:
                access_token = json.node.data.properties['auth_result']['access_token']
                file_info = json.node.data.properties['auth_result']['file_info']
                file_url = file_info["path"]
                file_name = file_info["name"]

                boundary = '---boundary'
                metadata = {"name": file_name}

                file_content_request = Request(
                    url=file_url, 
                    Method=Request.Method.get)
                file_content_response = await file_content_request.execute()
                file_content = file_content_response.content

                body = get_request_body(boundary, file_content, metadata)

                url = URL_UPLOAD
                
                headers = {
                    'Content-Type': f"multipart/related; boundary={boundary}",
                    'Authorization': f'Bearer {access_token}'}

   
                request = Request(
                    url=url,
                    method=Request.Method.post,
                    headers=headers,
                    data=body
                    )
            
                result = await request.execute()

                await json.save_result({
                    "result": result.status_code,
                    "access_token": access_token
                    })

                json.state = RunState.complete
            
            # Получение списка файлов
            if node_action == NodeAction.get_file_list:
                access_token = json.node.data.properties['auth_result']['access_token']

                url = URL_LIST

                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'}

                request = Request(
                    url=url,
                    method=Request.Method.get,
                    headers=headers
                    )
            
                result = await request.execute()
                result_data = result.json()

                await json.save_result({
                    "result": result_data
                    })

                json.state = RunState.complete

        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json
    