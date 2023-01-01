from brownie import (
    accounts,
    Contract,
    network,
    config,
)
from web3 import Web3
import eth_utils


FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMALS = 8
INITIAL_VALUE = 200000000000
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


# def get_breed(breed_number):
#     return BREED_MAPPING[breed_number]


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


# initializer=box.store, 1
def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeToAndCall(
                proxy.address,
                new_implementation_address,
                encode_function_data,
                {"from": account},
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    else:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                new_implementation_address,
                encode_function_call,
                {"from": account},
            )
        else:
            transaction = proxy.upgradeTo(new_implementation_address, {"from": account})
    return transaction


# contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}


# def deploy_mocks(decimals=DECIMALS, initial_vlaue=INITIAL_VALUE):
#     print(f"The active network is {network.show_active()}")
#     print("Deploying Mocks...")
#     account = get_account()
#     MockV3Aggregator.deploy(decimals, initial_vlaue, {"from": account})
#     link_token = LinkToken.deploy({"from": account})
#     print(f"Link token deployed to {link_token.address}")
#     vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
#     print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
#     print("Mocks Deployed!")


# def fund_with_link(
#     contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
# ):  # 0.1 Link
#     account = account if account else get_account()
#     link_token = link_token if link_token else get_contract("link_token")
#     tx = link_token.transfer(contract_address, amount, {"from": account})
#     # link_token_contract = interface.LinkTokenInterface(link_token.address)
#     # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
#     tx.wait(1)
#     print(f"Funded contract {contract_address} !")
#     return tx


# contract_to_mock = {
#     "eth_usd_price_feed": MockV3Aggregator,
#     "vrf_coordinator": VRFCoordinatorMock,
#     "link_token": LinkToken,
# }


# def get_contract(contract_name):
#     """
#     This function will grab the contract address from the brownie config
#     if defined, otherwise, it will deploy a mock version of that contract,
#     and return that mock contract.

#         Args:
#             contract_name (string)

#         Returns:
#             brownie.network.contract.ProjectContract: The most recently deployed
#             version of this contract
#     """
#     contract_type = contract_to_mock[contract_name]
#     if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
#         if len(contract_type) <= 0:
#             # MockV3Aggregator.length
#             deploy_mocks()
#         contract = contract_type[-1]  # MockV3Aggregator[-1]
#     else:
#         contract_address = config["networks"][network.show_active()][contract_name]
#         # address
#         # ABI
#         contract = Contract.from_abi(
#             contract_type._name, contract_address, contract_type.abi
#         )  # MockV3Aggregator.abi
#     return contract
