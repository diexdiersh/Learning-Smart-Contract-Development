from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    print(f"Current Account: {account}")
    if network.show_active() not in LOCAL_BLOCKHAIN_ENVIRONMENTS:
        print("Env is LIVE")
        price_feed_adress = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print("Env is LOCAL")
        deploy_mocks()
        price_feed_adress = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_adress,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    fund_me.tx.wait(1)
    print(f"Deployed Contract: {fund_me}")
    return fund_me


def main():
    deploy_fund_me()
