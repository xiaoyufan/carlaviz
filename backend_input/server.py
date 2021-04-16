import logging
from websocket_server import WebsocketServer

from carla_sender.game import Game


class Server:
	def __init__(self, args):
		self.args = args
		self.server = WebsocketServer(self.args.server_port,
					  host=self.args.server_host)

	def start_game(self):
		self.game = Game(self.args)
		self.game.start()

	def new_client(self, client, server):
		logging.info(f'A new client (id: {client["id"]}) has joined us.')
		self.start_game()

	def message_received(self, client, server, message):
		if not self.game:
			logging.warning('Game not started')
			return

		self.game.handle_input(message)

	def client_left(self, client, server):
		logging.info(f'A client (id: {client["id"]}) has left us.')
		self.game.end()

	def start(self):
		self.server.set_fn_new_client(self.new_client)
		self.server.set_fn_message_received(self.message_received)
		self.server.set_fn_client_left(self.client_left)

		self.server.run_forever()
