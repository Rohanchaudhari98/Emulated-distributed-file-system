a = "Select match_data.WinningTeam,sum(ball_data.total_run) from match_data,ball_data where match_data.ID=ball_data.ID group by match_data.WinningTeam"
b = "sum"
print(b in a)