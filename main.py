from swissround.tournament.Tournament import Tournament
from copy import deepcopy
from datagestion.evolution import evolution
from datagestion.io import io


def run(iteration):
	try:
		rank, toID = io.retrieve()
		generator = evolution.Generator(rank, 32)
	except FileNotFoundError:
		toID = 1
		rank = []
		generator = evolution.Generator(rank, 32)

	try:
		for i in range(iteration):
			for player in generator.ranking:
				player.hasPlayed.clear()
				player.score = 0

			tournament = Tournament(deepcopy(generator.ranking), Game, 7)
			for loop in range(tournament.nbRounds):
				tournament.createRound()
				tournament.playRound()
				tournament.updateRank()

			generator.ranking = deepcopy(tournament.ranking)
			io.logRank(generator.ranking, toID)
			generator.evol()
			toID += 1
			io.save(generator.ranking, toID)

	except KeyboardInterrupt:
		io.save(generator.ranking, toID)
