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
            # Prompt user for contract ID and retrieve corresponding contract
            contract_id = EventView.event_contract_id()
            contract = session.query(Contract).get(contract_id)

            # Check contract status and handle different scenarios
            if not contract.status:
                MainView.display_message(
                    f"Contract n°{contract.id} is not signed yet."
                )
                cls.create_event(
                    user, session
                )  # Recursively retry event creation
            elif contract.event is not None:
                MainView.display_message(
                    f"This contract already has an event attached to it."
                )
            else:
                # Prompt user for event details and create new event
                event_infos = EventView.create_event()
                (
                    event_name,
                    event_start,
                    event_end,
                    location,
                    attendees,
                    notes,
                ) = event_infos

                # Create event if user has the 'com' role, otherwise deny permission
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
                    contract.event = new_event
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
            # Retry creation upon encountering an exception
            callback = partial(cls.create_event, user, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def get_events(cls, user, session):
        from controllers.menus import MenusController

        try:
            # Retrieve all events with eager loading of related data
            events = (
                session.query(Event)
                .options(
                    joinedload(Event.contract),
                    joinedload(Event.support),
                )
                .all()
            )

            # Handle scenarios based on retrieved events or display message if none found
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
            # Display events based on user's role and handle corresponding actions
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

            # Return to main menu upon user's request
            if choice == "menu":
                callback = partial(
                    cls.events_permissions, user, events, session
                )
                MenusController.back_to_main_menu(user, session, callback)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Permission error : {e}")
            # Retry permission handling upon encountering an exception
            callback = partial(cls.events_permissions, user, events, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def edit_event(cls, user, events, session):
        from controllers.menus import MenusController

        try:
            # Prompt user for event ID and retrieve corresponding event
            event_id = EventView.get_event_id()
            event_to_edit = session.query(Event).get(event_id)

            # Handle different edit scenarios based on user's role and choices
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
                        # Prompt user for supervisor ID and update event support
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
                        # Prompt user for contract ID and update event contract
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
                        if new_contract.status == False:
                            session.rollback()
                            MainView.display_message(
                                f"contract n°{new_contract.id} is not signed"
                                " yet."
                            )
                            cls.edit_event(user, events, session)
                        else:
                            event_to_edit.contract = new_contract
                            session.commit()
                            MainView.display_message("Updated successfully.")
                            MenusController.main_menu(user, session)

                # Return to main menu upon user's request
                if choice == "menu":
                    callback = partial(cls.edit_event, user, events, session)
                    MenusController.back_to_main_menu(user, session, callback)
                else:
                    session.rollback()
                    MainView.display_message("Pick a valid option.")
                    cls.edit_event(
                        user, events, session
                    )  # Retry editing on invalid option

            else:
                MainView.display_message("No client found.")

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
            # Filter events based on user role ('man' or 'sup')
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

            # Handle scenarios based on filtered events or display message if none found
            if events:
                cls.events_permissions(user, events, session)
            else:
                MainView.display_message("No event found")
                MenusController.main_menu(user, session)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error filtering events : {e}")
            callback = partial(cls.filter_events, user, session)
            MenusController.back_to_main_menu(user, session, callback)
