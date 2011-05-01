for season in range(1950, 2011):
	race = Heat.objects.filter(type=Heat.RACE, date__year=season, results__position=1, results__dsq=False).count()
	qual = Heat.objects.filter(type=Heat.QUAL, date__year=season, results__position=1).count()
	grid = Heat.objects.filter(type=Heat.GRID, date__year=season, results__position=5).count()
	if race != qual != grid:
		print str(season) + ': ' + 'Qual:' + str(qual), 'Race:' + str(race), 'Grid:' + str(grid)
