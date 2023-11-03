import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request


class NodeType(flow.NodeType):
    id: str = '30f03eef-9e1f-4171-a75e-07656cf926fe'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'text_field'
    displayName: str = 'Текст5'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Текст5'
    properties: List[Property] = [
        Property(
            displayName='Текст5',
            name='text_field',
            type=Property.Type.JSON,
            placeholder='Text',
            description='Text',
            required=True,
            default='Text data',
        )
    ]
    

class NodeType2(flow.NodeType):
    id: str = '382063e6-edc3-47c7-9d92-c7d8f6fc8923'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'number_field'
    displayName: str = 'Число6'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Число6'
    properties: List[Property] = [
        Property(
            displayName='Число6',
            name='number_field',
            type=Property.Type.NUMBER,
            placeholder='Text',
            description='Text',
            required=True,
            default='Text data',
        )
    ]
    
class NodeType3(flow.NodeType):
    id: str = 'f3889166-b5fc-4b4f-b172-7846acdfdc9a'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'radio'
    displayName: str = 'Переключатель'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Переключатель'
    properties: List[Property] = [
        Property(
            displayName='Переключатель',
            name='radio',
            type=Property.Type.BOOLEAN,
            placeholder='Text',
            description='Text',
            required=True,
            default='Text data',
        )
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType
        
class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType2
        
class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType3

class Data:
    text_field = 0
    number_field = 0
    radio_type = False

class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            try: 
                # Ловит запрос от текстового поля
                Data.text_field = int(json.node.data.properties['text_field'])
            except:
                None
            try: 
                # Ловит запрос от числового поля
                Data.number_field = json.node.data.properties['number_field']
            except:
                None
            try:
                # Ловит запрос от переключателя
                Data.radio_type = json.node.data.properties['radio']
            except:
                None
            
            # Сумма двух полей
            sum: int = Data.text_field + Data.number_field
            
            if Data.radio_type:
                # Возвращает текстовый формат
                await json.save_result({
                    "result": str(sum)
                })
                json.state = RunState.complete
            else:  
                # Возвращает числовой формат
                await json.save_result({
                    "result": int(sum)
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
