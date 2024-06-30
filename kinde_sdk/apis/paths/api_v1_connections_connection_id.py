from kinde_sdk.paths.api_v1_connections_connection_id.get import ApiForget
from kinde_sdk.paths.api_v1_connections_connection_id.delete import ApiFordelete
from kinde_sdk.paths.api_v1_connections_connection_id.patch import ApiForpatch


class ApiV1ConnectionsConnectionId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
