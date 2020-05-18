import wptools
from datetime import datetime

def getNBASeasonStartEndDates(season):
	name = f"{season} NBA season"
	page = wptools.page(name, silent=True).get_parse(show=False)
	duration = page.data['infobox']["duration"]

	if season == "2019-20":
		split = duration.split("|")[1].split("(")[0].strip()
		start, end = split.split(" – ")
	else:
		split = duration.split("<br>")
		if len(split) == 1:
			start, end = duration.split("<br />")[0].strip().split(" – ")
		else:
			start, end = duration.split("<br>")[0].strip().split(" – ")

	date_fmt_parse = "%B %d, %Y"

	start_dt = datetime.strptime(start, date_fmt_parse)
	end_dt = datetime.strptime(end, date_fmt_parse)

	date_fmt_str = "%m/%d/%Y"

	start_str = start_dt.strftime(date_fmt_str)
	end_str = end_dt.strftime(date_fmt_str)

	return {"start": start_str, "end": end_str}

getNBASeasonStartEndDates("2019-20")