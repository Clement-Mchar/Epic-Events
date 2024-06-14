

class EventView:

    @classmethod
    def display_events(events, user):
        table = Table(show_header=True, header_style="cyan")
        table.add_column("ID", style="white", justify="right")
        table.add_column("Contract ID", style="white")
        table.add_column("Client Infos", style="white")
        table.add_column("Event Start", style="white")
        table.add_column("Event End", style="white")
        table.add_column("Support Contact", style="white")
        table.add_column("Location", style="white")
        table.add_column("Attendees", style="white")
        table.add_column("Notes", style="white")

        for event in events:
            client_infos = (
                f"Name: {event.client.full_name}, "
                f"Phone: {event.client.telephone}, "
                f"Email: {event.client.email}"
                if event.client
                else "N/A"
            )

            table.add_row(
                str(event.id),
                str(event.contract.id) if event.contract else "N/A",
                client_infos,
                event.event_start,
                event.event_end,
                (
                    event.support_contact.full_name
                    if event.support_contact
                    else "N/A"
                ),
                event.location,
                str(event.attendees),
                event.notes,
            )
        console.print(table)

        if user.role.code == "man":
            console.print("1. Display all events without support contact")
            console.print("2. Edit an event")
            choice = int(Prompt.ask("\nSelect an option"))
        if user.role.code == "sup":
            console.print("1. Display events that you are working on")
            console.print("2. Edit an event")
            choice = int(Prompt.ask("\nSelect an option"))

        return choice