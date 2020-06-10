from typing import Dict
import uuid


class AddressBookService:
    def __init__(
        self,
        config: Dict
    ) -> None:
        self.addrs: Dict[str, Dict] = {}

    def start(self):
        self.addrs = {}

    def stop(self):
        pass

    async def create_address(self, value: Dict) -> str:
        key = uuid.uuid4().hex
        self.addrs[key] = key
        return key

    async def get_address(self, key: str) -> Dict:
        return self.addrs[key]

    async def update_address(self, key: str, value: Dict) -> None:
        self.addrs[key] 
        self.addrs[key] = value

    async def delete_address(self, key: str) -> None:
        self.addrs[key]
        del self.addrs[key]

    async def get_all_addresses(self) -> Dict[str, Dict]:
        return self.addrs
