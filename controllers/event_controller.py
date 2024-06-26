from views.event_view import EventView
from views.menu_view import MainView
from views.user_view import UserView
from models.models import Event, Contract, User, Role, Client
from sqlalchemy.orm import joinedload
from functools import partial
import sentry_sdk


class EventController:

    @classmethod
    def create_event(cls, user, session):
        from controllers.menus import MenusController

        try:
            contract_id = EventView.event_contract_id()
            contract = session.query(Contract).get(contract_id)
            if contract.status == False:
                MainView.display_message(
                    f"Contract n°{contract.id} is not signed yet."
                )
                cls.create_event(user, session)
            elif contract.event != None:
                MainView.display_message(
                    f"This contract already have an event attached to it."
                )
            else:
                event_infos = EventView.create_event()
                (
                    event_name,
                    event_start,
                    event_end,
                    location,
                    attendees,
                    notes,
                ) = event_infos
                if user.role.code == "com":
                    new_event = Event(
                        contract_id=contract.id,
                        event_name=event_name,
                        event_start=event_start,
                        event_end=event_end,
                        location=location,
                        attendees=attendees,
                        notes=notes,
                    )
                    session.add(new_event)
                    contract.event == new_event
                    session.commit()
                    MainView.display_message(
                        f"Event created with id: {new_event.id}"
                    )
                else:
                    MainView.display_message(
                        "You don't have the permission to create an event."
                    )
                    return MenusController.main_menu(user, session)

        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error creating event : {e}")
            callback = partial(cls.create_event, user, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def get_events(cls, user, session):
        from controllers.menus import MenusController

        try:
            events = (
                session.query(Event)
                .options(
                    joinedload(Event.contract),
                    joinedload(Event.support),
                )
                .all()
            )
            if events:
                cls.events_permissions(user, events, session)
            else:
                MainView.display_message("No events found")
        except Exception as e:
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error getting events : {e}")
            callback = partial(cls.get_events, user, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def events_permissions(cls, user, events, session):
        from controllers.menus import MenusController

        try:
            choice = EventView.display_events(events, user)
            if user.role.code == "man":
                if choice == "1":
                    cls.filter_events(user, session)
                elif choice == "2":
                    cls.edit_event(user, events, session)
            elif user.role.code == "sup":
                if choice == "1":
                    cls.filter_events(user, session)
                elif choice == "2":
                    cls.edit_event(user, events, session)
            if choice == "menu":
                callback = partial(
                    cls.events_permissions, user, events, session
                )
                MenusController.back_to_main_menu(user, session, callback)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Permission error : {e}")
            callback = partial(cls.events_permissions, user, events, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def edit_event(cls, user, events, session):
        from controllers.menus import MenusController

        try:
            event_id = EventView.get_event_id()
            event_to_edit = session.query(Event).get(event_id)
            if event_to_edit:
                choice = EventView.edit_event_view(user)
                if user.role.code == "sup":
                    if choice == "1":
                        new_event_name = EventView.edit_event_name()
                        event_to_edit.event_name = new_event_name
                        session.commit()
                        MainView.display_message("Updated successfully.")
                        MenusController.main_menu(user, session)
                    elif choice == "2":
                        new_event_start = EventView.edit_event_start()
                        event_to_edit.event_start = new_event_start
                        session.commit()
                        MainView.display_message("Updated successfully.")
                        MenusController.main_menu(user, session)
                    elif choice == "3":
                        new_event_end = EventView.edit_event_end()
                        event_to_edit.event_end = new_event_end
                        session.commit()
                        MainView.display_message("Updated successfully.")
                        MenusController.main_menu(user, session)
                    elif choice == "4":
                        new_location = EventView.edit_event_location()
                        event_to_edit.location = new_location
                        session.commit()
                        MainView.display_message("Updated successfully.")
                        MenusController.main_menu(user, session)
                    elif choice == "5":
                        new_attendees = EventView.edit_event_attendees()
                        event_to_edit.attendees = new_attendees
                        session.commit()
                        MainView.display_message("Updated successfully.")
                        MenusController.main_menu(user, session)
                    elif choice == "6":
                        new_event_notes = EventView.edit_event_notes()
                        event_to_edit.notes = new_event_notes
                        session.commit()
                        MainView.display_message("Updated successfully.")
                        MenusController.main_menu(user, session)
                elif user.role.code == "man":
                    if choice == "1":
                        users = (
                            session.query(User)
                            .options(joinedload(User.role))
                            .join(User.role)
                            .filter(Role.code == "sup")
                            .all()
                        )
                        new_support_id = EventView.edit_event_support(users)
                        new_support = session.query(User).get(new_support_id)
                        event_to_edit.support = new_support
                        session.commit()
                        MainView.display_message("Updated successfully.")
                        MenusController.main_menu(user, session)
                    if choice == "2":
                        contracts = (
                            session.query(Contract)
                            .options(joinedload(Contract.client))
                            .join(Contract.client)
                            .all()
                        )
                        new_contract_id = EventView.edit_event_contract(
                            contracts
                        )
                        new_contract = session.query(Contract).get(
                            new_contract_id
                        )
                        event_to_edit.contract = new_contract
                        session.commit()
                        MainView.display_message("Updated successfully.")
                        MenusController.main_menu(user, session)
                if choice == "menu":
                    callback = partial(cls.edit_event, user, events, session)
                    MenusController.back_to_main_menu(user, session, callback)
                else:
                    session.rollback()
                    MainView.display_message("Pick a valid option.")
                    cls.edit_event(user, events, session)
            else:
                MainView.display_message("No client found.")
                cls.edit_event(user, events, session)
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"error editing event : {e}")
            callback = partial(cls.edit_event, user, events, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def filter_events(cls, user, session):
        from controllers.menus import MenusController

        try:
            if user.role.code == "man":
                events = (
                    session.query(Event)
                    .filter(Event.support == None)
                    .options(
                        joinedload(Event.support),
                        joinedload(Event.contract),
                    )
                    .all()
                )
                if events:
                    cls.events_permissions(user, events, session)
                else:
                    MainView.display_message("No event found")
                    MenusController.main_menu(user, session)
            elif user.role.code == "sup":
                events = (
                    session.query(Event)
                    .filter(Event.support_contact == user.id)
                    .options(
                        joinedload(Event.support),
                        joinedload(Event.contract),
                    )
                    .all()
                )
                if events:
                    cls.events_permissions(user, events, session)
                else:
                    MainView.display_message("No event found")
                    MenusController.main_menu(user, session)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error filtering events : {e}")
            callback = partial(cls.filter_events, user, events, session)
            MenusController.back_to_main_menu(user, session, callback)
