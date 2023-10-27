from typing import List, Optional

from uc_flow_schemas import flow
from uc_flow_schemas.flow import (
    Property,
    CredentialProtocol,
)


class CredentialType(flow.CredentialType):
    id: str = "alfacrm_api_auth2"
    is_public: bool = True
    displayName: str = 'AlfaCRM API Auth'
    protocol: CredentialProtocol = CredentialProtocol.ApiKey
    protected_properties: List[Property] = []
    properties: List[Property] = [
        Property(
            displayName='hostname',
            name='hostname',
            type=Property.Type.STRING,
            default='',
        ),
        Property(
            displayName='id филиала',
            name='branch',
            type=Property.Type.NUMBER,
            default='',
        ),
        Property(
            displayName='email',
            name='email',
            type=Property.Type.EMAIL,
            default='',
        ),
        Property(
            displayName='API key',
            name='api_key',
            type=Property.Type.STRING,
            default='',
        ),
    ]
    extends: Optional[List[str]] = []
   # icon: Optional[str] = ICON