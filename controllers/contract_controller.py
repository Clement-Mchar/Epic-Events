from views.contract_view import ContractView
from views.menu_view import MainView
from models.models import Contract, Client
from functools import partial
from sqlalchemy.orm import joinedload
import sentry_sdk


class ContractController:

    @classmethod
    def create_contract(cls, user, clients, choice, session):
        from controllers.menus import MenusController

        try:
            if choice == "menu":
                callback = partial(cls.create_contract, user, clients, session)
                MenusController.back_to_main_menu(user, session, callback)
            else:
                client = session.query(Client).get(choice)
                if client:
                    total_amount = ContractView.create_contract_view()
                    new_contract = Contract(
                        client_infos=client.id,
                        total_amount=total_amount,
                        left_amount=total_amount,
                    )
                    session.add(new_contract)
                    session.commit()
                    MainView.display_message(
                        f"Contract created with id: {new_contract.id}"
                    )
                else:
                    MainView.display_message("Pick a valid option")
                    cls.create_contract(user, clients, session)
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error creating contract: {e}")
            callback = partial(cls.create_contract, user, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def get_contracts(cls, user, session):
        from controllers.menus import MenusController

        try:
            contracts = (
                session.query(Contract)
                .options(joinedload(Contract.client))
                .all()
            )

            cls.contracts_permissions(user, contracts, session)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error getting contracts: {e}")
            callback = partial(cls.get_contracts, user, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def contracts_permissions(cls, user, contracts, session):
        from controllers.menus import MenusController
        from controllers.event_controller import EventController

        try:
            choice = ContractView.display_contracts(contracts, user)
            if user.role.code == "man":
                if choice == "1":
                    cls.edit_contract(user, contracts, session)
            elif user.role.code == "com":
                if choice == "1":
                    cls.edit_contract(user, contracts, session)
                elif choice in ["2", "3", "4"]:
                    cls.filter_contracts(user, contracts, choice, session)
                elif choice == "5":
                    EventController.create_event(user, session)
            if choice == "menu":
                callback = partial(cls.edit_contract, user, contracts, session)
                MenusController.back_to_main_menu(user, session, callback)
            else:
                MainView.display_message("Pick a valid option.")
                cls.edit_contract(user, contracts, session)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            MainView.display_message(
                f"Error getting contracts permissions : {e}"
            )
            callback = partial(
                cls.contracts_permissions, user, contracts, session
            )
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def edit_contract(cls, user, contracts, session):
        from controllers.menus import MenusController

        try:
            contract_id = ContractView.enter_contract_id()
            contract_to_edit = session.query(Contract).get(contract_id)
            if contract_to_edit:
                choice = ContractView.edit_contract_view(
                    user, contract_to_edit
                )
                if choice == "1":
                    new_total_amount = (
                        ContractView.edit_contract_total_amount()
                    )
                    contract_to_edit.total_amount = new_total_amount
                    contract_to_edit.left_amount = new_total_amount
                    session.commit()
                    MainView.display_message("Updated successfully.")
                    MenusController.main_menu(user, session)
                elif choice == "2":
                    new_amount_due = ContractView.edit_contract_amount_due()
                    contract_to_edit.left_amount = new_amount_due
                    session.commit()
                    MainView.display_message("Updated successfully.")
                    MenusController.main_menu(user, session)
                elif choice == "3":
                    new_status = ContractView.edit_contract_status()
                    if new_status == "yes":
                        contract_to_edit.status = True
                        session.commit()
                        MainView.display_message("Updated successfully.")
                        MenusController.main_menu(user, session)
                    if new_status == "no":
                        contract_to_edit.status = False
                        session.commit()
                        cls.get_contracts(user, session)
                elif choice == "menu":
                    callback = partial(
                        cls.edit_contract, user, contracts, session
                    )
                    MenusController.back_to_main_menu(user, session, callback)
                else:
                    session.rollback()
                    MainView.display_message("Pick a valid option.")
                    cls.edit_contract(user, contracts, session)
            else:
                MainView.display_message("No client found.")
                cls.edit_contract(user, contracts, session)
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error editing contract : {e}")
            callback = partial(cls.edit_contract, user, contracts, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def filter_contracts(cls, user, contracts, choice, session):
        from controllers.menus import MenusController

        try:
            if choice == "2":
                contracts = (
                    session.query(Contract)
                    .join(Client)
                    .filter(Client.commercial_contact == user.id)
                    .options(
                        joinedload(Contract.client).joinedload(
                            Client.commercial
                        )
                    )
                    .all()
                )
                if contracts:
                    cls.contracts_permissions(user, contracts, session)
                else:
                    MainView.display_message("No contract found")
                    MenusController.main_menu(user, session)
            if choice == "3":
                contracts = (
                    session.query(Contract)
                    .filter(Contract.left_amount > 0)
                    .all()
                )
                if contracts:
                    cls.contracts_permissions(user, contracts, session)
                else:
                    MainView.display_message("No contract found")
                    MenusController.main_menu(user, session)
            if choice == "4":
                contracts = (
                    session.query(Contract)
                    .filter(Contract.status == False)
                    .all()
                )
                if contracts:
                    ContractView.display_user_contracts(contracts)
                    callback = partial(
                        cls.filter_contracts, user, contracts, choice, session
                    )
                    MenusController.back_to_main_menu(user, session, callback)
                else:
                    MainView.display_message("No contract found")
                    MenusController.main_menu(user, session)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error filtering contracts : {e}")
            callback = partial(
                cls.filter_contracts, user, contracts, choice, session
            )
            MenusController.back_to_main_menu(user, session, callback)
