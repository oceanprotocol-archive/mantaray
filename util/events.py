
TIMEOUT = 20


def subscribe_event(event_func_name, keeper, agreement_id):
    event_map[event_func_name](keeper, agreement_id)


def _log_event(event_name):
    def _process_event(_):
        print(f'Received event {event_name}.')

    return _process_event


def subscribe_agreement_created_event(keeper, agreement_id):
    event = keeper.agreement_manager.subscribe_agreement_created(
        agreement_id,
        TIMEOUT,
        _log_event('EscrowAccessSecretStoreTemplate.AgreementCreated'),
        (),
        from_block=0,
        wait=True
    )
    assert event, 'no event for EscrowAccessSecretStoreTemplate.AgreementCreated'


def subscribe_fulfilled_lock_reward_condition(keeper, agreement_id):
    event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
        agreement_id,
        TIMEOUT,
        _log_event('LockRewardCondition.Fulfilled'),
        (),
        from_block=0,
        wait=True
    )
    assert event, 'no event for LockRewardCondition.Fulfilled'


def subscribe_fulfilled_access_secret_store_condition(keeper, agreement_id):
    event = keeper.access_secret_store_condition.subscribe_condition_fulfilled(
        agreement_id,
        TIMEOUT,
        _log_event('AccessSecretStoreCondition.Fulfilled'),
        (),
        from_block=0,
        wait=True
    )
    assert event, 'no event for AccessSecretStoreCondition.Fulfilled'


def subscribe_fulfilled_escrow_reward(keeper, agreement_id):
    event = keeper.escrow_reward_condition.subscribe_condition_fulfilled(
        agreement_id,
        TIMEOUT,
        _log_event('EscrowReward.Fulfilled'),
        (),
        from_block=0,
        wait=True
    )
    assert event, 'no event for EscrowReward.Fulfilled'


event_map = {
    "created agreement": subscribe_agreement_created_event,
    "lock reward": subscribe_fulfilled_lock_reward_condition,
    "access secret store": subscribe_fulfilled_access_secret_store_condition,
    "escrow reward": subscribe_fulfilled_escrow_reward,
}
