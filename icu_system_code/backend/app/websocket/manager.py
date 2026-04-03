class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, int] = {}

    def connect(self, patient_id: int) -> None:
        self.active_connections[patient_id] = self.active_connections.get(patient_id, 0) + 1

    def disconnect(self, patient_id: int) -> None:
        current = self.active_connections.get(patient_id, 0)
        if current <= 1:
            self.active_connections.pop(patient_id, None)
            return
        self.active_connections[patient_id] = current - 1
