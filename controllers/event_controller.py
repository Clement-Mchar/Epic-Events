class EventController:

    @classmethod
    def create_event(cls, user, session):
        from controllers.menus import MenusController
        event_infos = CommercialView.create_event(user)

    @classmethod
    def get_events(cls, user, session):
        events = (
            session.query(Event)
            .options(
                joinedload(Event.contract),
                joinedload(Event.client),
                joinedload(Event.support_contact),
            )
            .all()
        )
        MainView.display_events(events, user)
