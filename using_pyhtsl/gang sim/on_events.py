from pyhtsl import goto, IfOr, cancel_event, IsItem, Else, trigger_function, pause_execution
from everything import Items


def on_player_join() -> None:
    goto('event', 'Player Join')
    trigger_function('On Player Join')


def on_player_leave() -> None:
    goto('event', 'Player Quit')
    trigger_function('On Player Leave')


def on_player_kill() -> None:
    goto('event', 'Player Kill')
    trigger_function('On Player Kill')


def on_player_damage() -> None:
    goto('event', 'Player Damage')
    trigger_function('On Player Damage')


def on_player_death() -> None:
    goto('event', 'Player Death')
    trigger_function('On Player Death')


def on_player_enter_portal() -> None:
    goto('event', 'Player Enter Portal')
    pause_execution(4)
    trigger_function('On Player Enter Portal')


def on_player_drop_item() -> None:
    goto('event', 'Player Drop Item')
    with IfOr(
        *(IsItem(crown) for crown in (
            Items.bloods_leader_crown.item,
            Items.crips_leader_crown.item,
            Items.kings_leader_crown.item,
            Items.grapes_leader_crown.item,
        )),
    ):
        pass
    with Else:
        cancel_event()


if __name__ == '__main__':
    on_player_join()
    on_player_leave()
    on_player_kill()
    on_player_damage()
    on_player_death()
    on_player_enter_portal()
    on_player_drop_item()
