import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request



class NodeType(flow.NodeType):
    id: str = '89490712-0453-44ac-bbf4-680ae7b26080'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'Sum_node'
    displayName: str = 'Sum_node'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Складывает 2 числа, данные в формате строки и числа'
    properties: List[Property] = [
        Property(
            displayName='Число в формате строки',
            name='text_field',
            type=Property.Type.STRING,
            default = '0',
            description='Принимает число в формате строки',
            required=True,
        ),
        Property(
            displayName='Число',
            name='number_field',
            type=Property.Type.NUMBER,
            default = 0,
            description='Принимает число в числовом формате',
            required=True
        ),
         Property(
            displayName='Вернуть как число',
            name='switch',
            type=Property.Type.BOOLEAN,
            description='Вернуть в формате строки или числа',
            required=False,
            default=False,
        )
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            try:
                number1 = int(json.node.data.properties['text_field'])
            except ValueError:
                raise ValueError('В первом поле должно быть число в формате строки, допустимые символы 1234567890')
            number2 = json.node.data.properties['number_field']
            number_sum = number1 + number2
            
            if not json.node.data.properties['switch']:
                number_sum = str(number_sum)

            await json.save_result({
                "result": number_sum
            })
            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
