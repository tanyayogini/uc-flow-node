import ujson
import requests
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState, DisplayOptions, OptionValue
from uc_http_requester.requester import Request
from node.credential_type import CredentialType
from node.enums import NodeAction, Resource, Operation, Parameters
from node.parameters_converter import parameters_converter

URL_LOGIN = 'auth/login'
URL_GET_CUSTOMER = 'customer/index'
URL_CREATE_CUSTOMER = 'customer/create'
URL_UPDATE_CUSTOMER = 'customer/update'


class NodeType(flow.NodeType):
    id: str = '6f0f309e-5451-4a62-8a3a-7bca5404e6f8'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'My_alfacrm3'
    displayName: str = 'my_alfacrm3'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'alfacrm_node'
    properties: List[Property] = [
        Property(
            displayName='Действие кубика',
            name='node_action',
            type=Property.Type.OPTIONS,
            options=[
                OptionValue(
                    name='Авторизация',
                    value=NodeAction.auth,
                    description=''
                ),
                OptionValue(
                    name='Получение данных',
                    value=NodeAction.get_data,
                    description=''
                ),
            ]
        ),
        Property(
            displayName='url',
            name='hostname',
            type=Property.Type.STRING,
            default='',
            displayOptions=DisplayOptions(
                show={
                    'node_action': [
                        NodeAction.auth
                    ],
                },
            ), 
        ),
        Property(
            displayName='id филиала',
            name='branch',
            type=Property.Type.NUMBER,
            default='',
            displayOptions=DisplayOptions(
                show={
                    'node_action': [
                        NodeAction.auth
                    ],
                },
            ), 
        ),
        Property(
            displayName='email',
            name='email',
            type=Property.Type.EMAIL,
            default='',
            displayOptions=DisplayOptions(
                show={
                    'node_action': [
                        NodeAction.auth
                    ],
                },
            ), 
        ),
        Property(
            displayName='API key',
            name='api_key',
            type=Property.Type.STRING,
            default='',
            displayOptions=DisplayOptions(
                show={
                    'node_action': [
                        NodeAction.auth
                    ],
                },
            ), 
        ),
        Property(
            displayName='auth_result',
            name='auth_result',
            type=Property.Type.JSON,
            displayOptions=DisplayOptions(
                show={
                    'node_action': [
                        NodeAction.get_data
                    ],
                },
            ),     
        ),
        Property(
            displayName='Resource',
            name='resource',
            type=Property.Type.OPTIONS,
            options=[
                OptionValue(
                    name='Customer',
                    value=Resource.customer,
                    description='',
                ),
            ],
            displayOptions=DisplayOptions(
                show={
                    'node_action': [
                        NodeAction.get_data
                    ],
                },
            ),      
        ),
        Property(
            displayName='Operation',
            name='operation',
            type=Property.Type.OPTIONS,
            options=[
                OptionValue(
                    name='index',
                    value=Operation.index_,
                    description='',
                ),
                OptionValue(
                    name='create',
                    value=Operation.create,
                    description='',
                ),
                OptionValue(
                    name='update',
                    value=Operation.update,
                    description='',
                ),
            ],
            displayOptions=DisplayOptions(
                show={
                     'node_action': [
                        NodeAction.get_data
                    ],
                    'resource': [
                        Resource.customer
                    ],
                },
            ),
        ),
        Property(
            displayName='Parameters',
            name='parameters',
            type=Property.Type.COLLECTION,
            default={},
            displayOptions=DisplayOptions(
                show={
                     'node_action': [
                        NodeAction.get_data
                    ],
                    'resource': [
                        Resource.customer,
                    ],
                    'operation': [
                        Operation.index_,
                        Operation.create,
                        Operation.update
                    ],
                }
            ),
            options=[
                Property(
                    displayName='id',
                    name=Parameters.id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id клиента',
                ),
                Property(
                    displayName='id_study',
                    name=Parameters.is_study,
                    type=Property.Type.NUMBER,
                    default='',
                    description='состояние клиента ( 0 - лид, 1 - клиент)',
                ),
                Property(
                    displayName='study_status_id',
                    name=Parameters.study_status_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id статуса клиента',
                ),
                Property(
                    displayName='name',
                    name=Parameters.name,
                    type=Property.Type.STRING,
                    default='',
                    description='имя клиента',
                ),
                Property(
                    displayName='gender',
                    name=Parameters.gender,
                    type=Property.Type.STRING,
                    default='',
                    description='пол клиента',
                ),
                Property(
                    displayName='age_from',
                    name=Parameters.age_from,
                    type=Property.Type.NUMBER,
                    default='',
                    description='возраст клиента от',
                ),
                Property(
                    displayName='age_to',
                    name=Parameters.age_to,
                    type=Property.Type.NUMBER,
                    default='',
                    description='возраст клиента до',
                ),
                Property(
                    displayName='phone',
                    name=Parameters.phone,
                    type=Property.Type.STRING,
                    default='',
                    description='контакты клиента',
                ),
                Property(
                    displayName='legal_type',
                    name=Parameters.legal_type,
                    type=Property.Type.NUMBER,
                    default='',
                    description='тип заказчика(1-физ лицо, 2-юр.лицо)',
                ),
                Property(
                    displayName='legal_name',
                    name=Parameters.legal_name,
                    type=Property.Type.STRING,
                    default='',
                    description='имя заказчика',
                ),
                Property(
                    displayName='company_id',
                    name=Parameters.company_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id юр лица',
                ),
                Property(
                    displayName='lesson_count_from',
                    name=Parameters.lesson_count_from,
                    type=Property.Type.NUMBER,
                    default='',
                    description='остаток уроков от',
                ),
                Property(
                    displayName='lesson_count_to',
                    name=Parameters.lesson_count_to,
                    type=Property.Type.NUMBER,
                    default='',
                    description='остаток уроков до',
                ),
                Property(
                    displayName='balance_contract_from',
                    name=Parameters.balance_contract_from,
                    type=Property.Type.NUMBER,
                    default='',
                    description='баланс договора от',
                ),
                Property(
                    displayName='balance_contract_to',
                    name=Parameters.balance_contract_to,
                    type=Property.Type.NUMBER,
                    default='',
                    description='баланс договора до',
                ),
                Property(
                    displayName='balance_bonus_from',
                    name=Parameters.balance_bonus_from,
                    type=Property.Type.NUMBER,
                    default='',
                    description='баланс бонусов от',
                ),
                Property(
                    displayName='balance_bonus_to',
                    name=Parameters.balance_bonus_to,
                    type=Property.Type.NUMBER,
                    default='',
                    description='баланс бонусов до',
                ),
                Property(
                    displayName='removed',
                    name=Parameters.removed,
                    type=Property.Type.NUMBER,
                    default='',
                    description='флаг архивности (2 - только архивные, 1 - активные и архивные, 0 – только активные)',
                ),
                Property(
                    displayName='removed_from',
                    name=Parameters.removed_from,
                    type=Property.Type.DATE,
                    default='',
                    description='дата отправки в архив от',
                ),
                Property(
                    displayName='removed_to',
                    name=Parameters.removed,
                    type=Property.Type.DATE,
                    default='',
                    description='дата отправки в архив',
                ),
                Property(
                    displayName='level_id',
                    name=Parameters.level_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id уровня знаний',
                ),
                Property(
                    displayName='assigned_id',
                    name=Parameters.assigned_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id ответственного менеджера',
                ),
                Property(
                    displayName='employee_id',
                    name=Parameters.employee_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id ответственного педагога',
                ),
                Property(
                    displayName='lead_source_id',
                    name=Parameters.lead_source_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id источника',
                ),
                Property(
                    displayName='color',
                    name=Parameters.color,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id цвета',
                ),
                Property(
                    displayName='note',
                    name=Parameters.note,
                    type=Property.Type.STRING,
                    default='',
                    description='примечание',
                ),
                Property(
                    displayName='date_from',
                    name=Parameters.date_from,
                    type=Property.Type.DATE,
                    default='',
                    description='дата добавления от',
                ),
                Property(
                    displayName='date_to',
                    name=Parameters.date_to,
                    type=Property.Type.DATE,
                    default='',
                    description='дата добавления до',
                ),
                Property(
                    displayName='next_lesson_date_from',
                    name=Parameters.next_lesson_date_from,
                    type=Property.Type.DATE,
                    default='',
                    description='дата след.посещения от',
                ),
                Property(
                    displayName='next_lesson_date_to',
                    name=Parameters.next_lesson_date_to,
                    type=Property.Type.DATE,
                    default='',
                    description='дата след.посещения до',
                ),
                Property(
                    displayName='tariff_till_from',
                    name=Parameters.tariff_till_from,
                    type=Property.Type.DATE,
                    default='',
                    description='дата действия абонемента от',
                ),
                Property(
                    displayName='tariff_till_to',
                    name=Parameters.tariff_till_to,
                    type=Property.Type.DATE,
                    default='',
                    description='дата действия абонемента до',
                ),
                Property(
                    displayName='customer_reject_id',
                    name=Parameters.customer_reject_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id причины отказа',
                ),
                Property(
                    displayName='comment',
                    name=Parameters.comment,
                    type=Property.Type.STRING,
                    default='',
                    description='комментарий',
                ),
                Property(
                    displayName='dob_from',
                    name=Parameters.dob_from,
                    type=Property.Type.DATE,
                    default='',
                    description='дата рождения от',
                ),
                Property(
                    displayName='dob_to',
                    name=Parameters.dob_to,
                    type=Property.Type.DATE,
                    default='',
                    description='дата рождения до',
                ),
                Property(
                    displayName='withGroups:true',
                    name=Parameters.withGroups_true,
                    type=Property.Type.STRING,
                    default='',
                    description='активные группы клиента',
                ),
                Property(
                    displayName='page',
                    name=Parameters.page,
                    type=Property.Type.NUMBER,
                    default='',
                    description='страница для пагинации',
                ),
            ]   
        ),
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            node_action = json.node.data.properties['node_action']

            # Авторизация
            if node_action == NodeAction.auth:
                hostname = json.node.data.properties['hostname']
                email = json.node.data.properties['email']
                api_key = json.node.data.properties['api_key']
                branch = json.node.data.properties['branch']

                url = f'https://{hostname}/v2api/{URL_LOGIN}'

                headers = {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                        }
            
                auth_data = {"email" : email,"api_key" : api_key}

                auth_request = Request(
                    url=url,
                    method=Request.Method.post,
                    json=auth_data,
                    headers=headers)
            
                auth_result = await auth_request.execute()

                auth_result_data = auth_result.json()
                token = auth_result_data['token']

                await json.save_result({
                    "token": token,
                    "branch": branch,
                    "hostname": hostname
                    })
                json.state = RunState.complete

            # Получение данных
            if node_action == NodeAction.get_data:
                customer_params = parameters_converter(json.node.data.properties['parameters'])
                token = json.node.data.properties['auth_result']['token']
                branch = json.node.data.properties['auth_result']['branch']
                hostname = json.node.data.properties['auth_result']['hostname']

                headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-ALFACRM-TOKEN': token}

                operation = json.node.data.properties['operation']

                if operation == Operation.index_:
                    url = f'https://{hostname}/v2api/{branch}/{URL_GET_CUSTOMER}'
                
                if operation == Operation.create:
                    url = f'https://{hostname}/v2api/{branch}/{URL_CREATE_CUSTOMER}'
                    customer_params["branch_ids"] = [branch]

                if operation == Operation.update:
                    id = customer_params.pop('id')
                    url = f'https://{hostname}/v2api/{branch}/{URL_UPDATE_CUSTOMER}?id={id}'

                data = Request(
                    url=url,
                    method=Request.Method.post,
                    json=customer_params,
                    headers=headers)

                result = await data.execute()

                await json.save_result({
                "result": result.json()
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
