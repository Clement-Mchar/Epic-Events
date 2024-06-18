from views.contract_view import ContractView
from views.menu_view import MainView
from models.models import Contract, Client
from functools import partial
from sqlalchemy.orm import joinedload


class ContractController:

    @classmethod
    def create_contract(cls, user, clients, choice, session):
        from controllers.menus import MenusController

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

    @classmethod
    def get_contracts(cls, user, session):
        try:
            contracts = (
                session.query(Contract)
                .options(joinedload(Contract.client))
                .all()
            )

            cls.contracts_permissions(user, contracts, session)
        except Exception as e:
            print(f"Error during get_contracts: {e}")

    @classmethod
    def contracts_permissions(cls, user, contracts, session):
        from controllers.menus import MenusController
        from controllers.event_controller import EventController
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

    @classmethod
    def edit_contract(cls, user, contracts, session):
        from controllers.menus import MenusController

        contract_id = ContractView.enter_contract_id(user)
        try:
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
            MainView.display_message("Please enter a valid ID.")
            cls.edit_contract(user, contracts, session)

    @classmethod
    def filter_contracts(cls, user, contracts, choice, session):
        from controllers.menus import MenusController

        if choice == "2":
            contracts = (
                session.query(Contract)
                .join(Client)
                .filter(Client.commercial_contact == user.id)
                .options(
                    joinedload(Contract.client).joinedload(Client.commercial)
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
                session.query(Contract).filter(Contract.left_amount > 0).all()
            )
            if contracts:
                cls.contracts_permissions(user, contracts, session)
            else:
                MainView.display_message("No contract found")
                MenusController.main_menu(user, session)
        if choice == "4":
            contracts = (
                session.query(Contract).filter(Contract.status == False).all()
            )
            if contracts:
                ContractView.display_user_contracts(contracts, user)
                callback = partial(
                    cls.filter_contracts, user, contracts, session
                )
                MenusController.back_to_main_menu(user, session, callback)
            else:
                MainView.display_message("No contract found")
                MenusController.main_menu(user, session)
