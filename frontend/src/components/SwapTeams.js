import React, { Fragment, useState } from 'react';
//useState https://reactjs.org/docs/hooks-state.html

const SwapTeams = () => {
	const [teamDescriptions, setTeamDescriptions] = useState([
		{
			teamName: 'Golden State Warriors',
			wins: 73,
			losses: 9,
			wlPercent: .890
		},
		{
			teamName: 'San Antonio Spurs',
			wins: 67,
			losses: 15,
			wlPercent: .817
		},
		{
			teamName: 'Cleveland Cavaliers',
			wins: 57,
			losses: 25,
			wlPercent: '.695'
		},
		{
			teamName: 'Toronto Raptors',
			wins: 56,
			losses: 26,
			wlPercent: '.683'
		},
		{
			teamName: 'Oklahoma City Thunder',
			wins: 55,
			losses: 27,
			wlPercent: .671 
		},
		{
			teamName: 'LA Clippers',
			wins: 53,
			losses: 29,
			wlPercent: .646
		},
		{
			teamName: 'Miami Heat',
			wins: 48,
			losses: 34,
			wlPercent: .585
		},
		{
			teamName: 'Atlanta Hawks',
			wins: 48,
			losses: 34,
			wlPercent: .585
		},
		{
			teamName: 'Boston Celtics',
			wins: 48,
			losses: 34,
			wlPercent: .585 
		},
		{
			teamName: 'Charlotte Hornets',
			wins: 48,
			losses: 34,
			wlPercent: .585 
		},
		{
			teamName: 'Indiana Pacers',
			wins: 45,
			losses: 37,
			wlPercent: .549
		},
		{
			teamName: 'Portland Trail Blazers',
			wins: 44,
			losses: 38,
			wlPercent: .537 
		},	
		{
			teamName: 'Detroit Pistons',
			wins: 44,
			losses: 38,
			wlPercent: .537 
		},	
		{
			teamName: 'Dallas Mavericks',
			wins: 42,
			losses: 40,
			wlPercent: .512
		},	
		{
			teamName: 'Dallas Mavericks',
			wins: 42,
			losses: 40,
			wlPercent: .512
		},	
		{
			teamName: 'Memphis Grizzlies',
			wins: 42,
			losses: 40,
			wlPercent: .512
		},	
		{
			teamName: 'Chicago Bulls',
			wins: 42,
			losses: 40,
			wlPercent: .512
		},	
		{
			teamName: 'Houston Rockets',
			wins: 41,
			losses: 41,
			wlPercent: .500
		},	
		{
			teamName: 'Washington Wizards',
			wins: 41,
			losses: 41,
			wlPercent: .500
		}
	]);
	/*	
	const [predictions, setPredictions] = useState([
		{
			date: '10/16/2018',
			home: 'Boston Celtics',
			away: 'Philadelphia 76ers',
			prediction: 0,
			actual: 0
		}
	]);
	*/
	const [predictions, setPredictions] = useState([{'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Los Angeles Clippers', 'date': '10/19/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Phoenix Suns', 'date': '10/20/2017', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 New Orleans Pelicans', 'date': '10/22/2017', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Washington Wizards', 'date': '10/25/2017', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Toronto Raptors', 'date': '10/27/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Utah Jazz', 'date': '10/28/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Detroit Pistons', 'date': '10/31/2017', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Portland Trail Blazers', 'date': '11/02/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Brooklyn Nets', 'date': '11/03/2017', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Memphis Grizzlies', 'date': '11/05/2017', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Boston Celtics', 'date': '11/08/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Washington Wizards', 'date': '11/09/2017', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Milwaukee Bucks', 'date': '11/11/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Phoenix Suns', 'date': '11/13/2017', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Philadelphia 76ers', 'date': '11/15/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Phoenix Suns', 'date': '11/17/2017', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Denver Nuggets', 'date': '11/19/2017', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Chicago Bulls', 'date': '11/21/2017', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Sacramento Kings', 'date': '11/22/2017', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Los Angeles Clippers', 'date': '11/27/2017', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Golden State Warriors', 'date': '11/29/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Denver Nuggets', 'date': '12/02/2017', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Houston Rockets', 'date': '12/03/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Philadelphia 76ers', 'date': '12/07/2017', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Charlotte Hornets', 'date': '12/09/2017', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 New York Knicks', 'date': '12/12/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Cleveland Cavaliers', 'date': '12/14/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Golden State Warriors', 'date': '12/18/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Houston Rockets', 'date': '12/20/2017', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Golden State Warriors', 'date': '12/22/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Portland Trail Blazers', 'date': '12/23/2017', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Minnesota Timberwolves', 'date': '12/25/2017', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Memphis Grizzlies', 'date': '12/27/2017', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Los Angeles Clippers', 'date': '12/29/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Houston Rockets', 'date': '12/31/2017', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Minnesota Timberwolves', 'date': '01/01/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Oklahoma City Thunder', 'date': '01/03/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Charlotte Hornets', 'date': '01/05/2018', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Atlanta Hawks', 'date': '01/07/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Sacramento Kings', 'date': '01/09/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 San Antonio Spurs', 'date': '01/11/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Dallas Mavericks', 'date': '01/13/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Memphis Grizzlies', 'date': '01/15/2018', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Oklahoma City Thunder', 'date': '01/17/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Indiana Pacers', 'date': '01/19/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 New York Knicks', 'date': '01/21/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Boston Celtics', 'date': '01/23/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Chicago Bulls', 'date': '01/26/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Toronto Raptors', 'date': '01/28/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Orlando Magic', 'date': '01/31/2018', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Brooklyn Nets', 'date': '02/02/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Oklahoma City Thunder', 'date': '02/04/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Phoenix Suns', 'date': '02/06/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Oklahoma City Thunder', 'date': '02/08/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Dallas Mavericks', 'date': '02/10/2018', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 New Orleans Pelicans', 'date': '02/14/2018', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Minnesota Timberwolves', 'date': '02/15/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Dallas Mavericks', 'date': '02/23/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Sacramento Kings', 'date': '02/24/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Atlanta Hawks', 'date': '02/26/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Miami Heat', 'date': '03/01/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 San Antonio Spurs', 'date': '03/03/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Portland Trail Blazers', 'date': '03/05/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Orlando Magic', 'date': '03/07/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Denver Nuggets', 'date': '03/09/2018', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Cleveland Cavaliers', 'date': '03/11/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Denver Nuggets', 'date': '03/13/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Golden State Warriors', 'date': '03/14/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Miami Heat', 'date': '03/16/2018', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Indiana Pacers', 'date': '03/19/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 New Orleans Pelicans', 'date': '03/22/2018', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Memphis Grizzlies', 'date': '03/24/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Detroit Pistons', 'date': '03/26/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Dallas Mavericks', 'date': '03/28/2018', 'prediction': 1, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Milwaukee Bucks', 'date': '03/30/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Sacramento Kings', 'date': '04/01/2018', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Utah Jazz', 'date': '04/03/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 San Antonio Spurs', 'date': '04/04/2018', 'prediction': 0, 'actual': 0}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Minnesota Timberwolves', 'date': '04/06/2018', 'prediction': 1, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Utah Jazz', 'date': '04/08/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Houston Rockets', 'date': '04/10/2018', 'prediction': 0, 'actual': 1}, {'home': '2017-18 Los Angeles Lakers', 'away': '2017-18 Los Angeles Clippers', 'date': '04/11/2018', 'prediction': 0, 'actual': 0}]



	);

//jsondata.predictions [{"home": "Boston Celtics", "away": "Philadelphia 76ers", "date": "10/28/2015", "prediction": 1, "actual": 0}, {"home": "Boston Celtics", "away": "Toronto Raptors", "date": "10/30/2015", "prediction": 0, "actual": 1}, {"home": "Boston Celtics", "away": "San Antonio Spurs", "date": "11/01/2015", "prediction": 1, "actual": 1}, {"home": "Boston Celtics", "away": "Indiana Pacers", "date": "11/04/2015", "prediction": 1, "actual": 1}, 

	let teamList = ['Atlanta Hawks','2019-20','Atlanta Hawks','2019-20']

	const onSubmitForm = async e => {
		e.preventDefault();
		//console.log('teamDescriptions',teamDescriptions);
		//console.log('teamList', teamList);
		const body = { teamList: teamList };

		console.log('teamList', teamList);


		const response = await fetch('/standings',{
			method: 'POST',
			headers: { 'Content-Type': 'application/json'},
			body: JSON.stringify(body)
		});
		const jsonData = await response.json();

		console.log('jsondata',jsonData);
		console.log('jsondata.predictions', jsonData.listOfPredictions);

		setPredictions(jsonData.listOfPredictions)

		//setPredictions(jsonData.predictions);
		//console.log('test',jsonData.test);
		//setTeamDescriptions(teamDescriptions+1);
		/*
		setTeamDescriptions([
			{
				teamName: 'Golden State Warriors',
				wins: 73,
				losses: 9,
				wlPercent: .890
			},
			{
				teamName: 'San Antonio Spurs',
				wins: 67,
				losses: 15,
				wlPercent: .817
			},
			{
				teamName: 'Cleveland Cavaliers',
				wins: 57,
				losses: 25,
				wlPercent: '.695'
			}
		])
		*/
		//console.log(jsonData.predictions);
	}

	return(
		<Fragment>
			<h2 className='text-center'>Swap Teams To View Simulated Standings</h2>
		    <form  onSubmit={ onSubmitForm }>
			    <div className="row">
    		  		<div className="col-sm text-center">
						<h3>Team to swap out</h3>
							<select onChange={e => teamList[0]=(e.target.value)}>
							  <option value="Atlanta Hawks">Atlanta Hawks</option>
							  <option value="Boston Celtics">Boston Celtics</option>
							  <option value="Brooklyn Nets">Brooklyn Nets</option>
							  <option value="Charlotte Hornets">Charlotte Hornets</option>
							  <option value="Chicago Bulls">Chicago Bulls</option>
							  <option value="Cleveland Cavaliers">Cleveland Cavaliers</option>
							  <option value="Dallas Mavericks">Dallas Mavericks</option>
							  <option value="Golden State Warriors">Golden State Warriors</option>
							  <option value="Houston Rockets">Houston Rockets</option>
							  <option value="Indiana Pacers">Indiana Pacers</option>
							  <option value="Los Angeles Clippers">Los Angeles Clippers</option>
							  <option value="Los Angeles Lakers">Los Angeles Lakers</option>
							  <option value="Memphis Grizzlies">Memphis Grizzlies</option>
							  <option value="Miami Heat">Miami Heat</option>
							  <option value="Milwaukee Bucks">Milwaukee Bucks</option>
							  <option value="Minnesota Timberwolves">Minnesota Timberwolves</option>
							  <option value="New Orleans Hornets">New Orleans Hornets</option>
							  <option value="New York Knicks">New York Knicks</option>
							  <option value="Oklahoma City Thunder">Oklahoma City Thunder</option>
							  <option value="Orlando Magic">Orlando Magic</option>
							  <option value="Philadelphia Sixers">Philadelphia Sixers</option>
							  <option value="Phoenix Suns">Phoenix Suns</option>
							  <option value="Portland Trail Blazers">Portland Trail Blazers</option>
							  <option value="Sacramento Kings">Sacramento Kings</option>
							  <option value="San Antonio Spurs">San Antonio Spurs</option>
							  <option value="Toronto Raptors">Toronto Raptors</option>
							  <option value="Utah Jazz">Utah Jazz</option>
							  <option value="Washington Wizards">Washington Wizards</option>
							</select>

							<select className="ml-1" onChange={e => teamList[1]=(e.target.value)}>
							    <option value="2019-20">2019-20</option>
							    <option value="2018-19">2018-19</option>
							    <option value="2017-18">2017-18</option>
							    <option value="2016-17">2016-17</option>
							    <option value="2015-16">2015-16</option>
							    <option value="2014-15">2014-15</option>
							</select>
					</div>

    		  		<div className="col-sm text-center">
						<h3>Team to swap in</h3>
							<select onChange={e => teamList[2]=(e.target.value)}>
							  <option value="Atlanta Hawks">Atlanta Hawks</option>
							  <option value="Boston Celtics">Boston Celtics</option>
							  <option value="Brooklyn Nets">Brooklyn Nets</option>
							  <option value="Charlotte Hornets">Charlotte Hornets</option>
							  <option value="Chicago Bulls">Chicago Bulls</option>
							  <option value="Cleveland Cavaliers">Cleveland Cavaliers</option>
							  <option value="Dallas Mavericks">Dallas Mavericks</option>
							  <option value="Golden State Warriors">Golden State Warriors</option>
							  <option value="Houston Rockets">Houston Rockets</option>
							  <option value="Indiana Pacers">Indiana Pacers</option>
							  <option value="Los Angeles Clippers">Los Angeles Clippers</option>
							  <option value="Los Angeles Lakers">Los Angeles Lakers</option>
							  <option value="Memphis Grizzlies">Memphis Grizzlies</option>
							  <option value="Miami Heat">Miami Heat</option>
							  <option value="Milwaukee Bucks">Milwaukee Bucks</option>
							  <option value="Minnesota Timberwolves">Minnesota Timberwolves</option>
							  <option value="New Orleans Hornets">New Orleans Hornets</option>
							  <option value="New York Knicks">New York Knicks</option>
							  <option value="Oklahoma City Thunder">Oklahoma City Thunder</option>
							  <option value="Orlando Magic">Orlando Magic</option>
							  <option value="Philadelphia Sixers">Philadelphia Sixers</option>
							  <option value="Phoenix Suns">Phoenix Suns</option>
							  <option value="Portland Trail Blazers">Portland Trail Blazers</option>
							  <option value="Sacramento Kings">Sacramento Kings</option>
							  <option value="San Antonio Spurs">San Antonio Spurs</option>
							  <option value="Toronto Raptors">Toronto Raptors</option>
							  <option value="Utah Jazz">Utah Jazz</option>
							  <option value="Washington Wizards">Washington Wizards</option>
							</select>

							<select className="ml-1"  onChange={e => teamList[3]=(e.target.value)}>
							    <option value="2019-20">2019-20</option>
							    <option value="2018-19">2018-19</option>
							    <option value="2017-18">2017-18</option>
							    <option value="2016-17">2016-17</option>
							    <option value="2015-16">2015-16</option>
							    <option value="2014-15">2014-15</option>
							</select>
					</div>

				</div>
				<div className="row justify-content-center">
				    <button type="submit" className="btn btn-primary">Submit</button>
				</div>
			</form>

			<h2 className='text-center mt-4'>Standings</h2>
			<table className="table table-striped">
			    <thead>
			    	<tr>
			        	<th>Team Name</th>
			        	<th>Wins</th>
			        	<th>Losses</th>
			        	<th>Win/Loss PCT</th>
			    	</tr>
			    </thead>
			    <tbody>
			      	{teamDescriptions.map((team,index) => (
			      		<tr key={index} index={index}>
			      			<td>{team.teamName}</td>
			      			<td>{team.wins}</td>
			      			<td>{team.losses}</td>
			      			<td>{team.wlPercent}</td>
			      		</tr>
			      	))}
			    </tbody>
			</table>

			<h2 className='text-center mt-4'>Predicted Games</h2>
			<table className="table table-striped">
			    <thead>
			    	<tr>
			        	<th>Date</th>
			        	<th>Home</th>
			        	<th>Away</th>
			        	<th>Prediction</th>
			        	<th>Actual</th>
			    	</tr>
			    </thead>
			    <tbody>
			      	{predictions.map((game,index) => (
			      		<tr key={index} index={index}>
			      			<td>{game.date}</td>
			      			<td>{game.home}</td>
			      			<td>{game.away}</td>
			      			<td>{game.prediction}</td>
			      			<td>{game.actual}</td>
			      		</tr>
			      	))}
			    </tbody>
			</table>

		</Fragment>
	); 

};

export default SwapTeams;

/*  


Previous Code:
---------- Specific team name from teamDescription
			<p>Counter {teamDescriptions[0].teamName}</p>

// --------------- DROP DOWN ------
							<div className="dropdown">
								<button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							    	Select Team
							 	</button>
								<div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
							    	<a className="dropdown-item" href="#">Atlanta Hawks</a>
							    	<a className="dropdown-item" href="#">Boston Celtics</a>
							    	<a className="dropdown-item" href="#">Brooklyn Nets</a>
							    	<a className="dropdown-item" href="#">Charlotte Hornets</a>
							    	<a className="dropdown-item" href="#">Chicago Bulls</a>
							    	<a className="dropdown-item" href="#">Cleveland Cavaliers</a>
							    	<a className="dropdown-item" href="#">Dallas Mavericks</a>
							    	<a className="dropdown-item" href="#">Denver Nuggets</a>
							    	<a className="dropdown-item" href="#">Golden State Warriors</a>
							    	<a className="dropdown-item" href="#">Houston Rockets</a>
							    	<a className="dropdown-item" href="#">Indiana Pacers</a>
							    	<a className="dropdown-item" href="#">LA Clippers</a>
							    	<a className="dropdown-item" href="#">LA Lakers</a>
							    	<a className="dropdown-item" href="#">Memphis Grizzlies</a>
							    	<a className="dropdown-item" href="#">Miami Heat</a>
							    	<a className="dropdown-item" href="#">Milwaukee Bucks</a>
							    	<a className="dropdown-item" href="#">Minnesota Timberwolves</a>
							    	<a className="dropdown-item" href="#">New Orleans Hornets</a>
							    	<a className="dropdown-item" href="#">New York Knicks</a>
							    	<a className="dropdown-item" href="#">Oklahoma City Thunder</a>
							    	<a className="dropdown-item" href="#">Orlando Magic</a>
							    	<a className="dropdown-item" href="#">Philadelphia Sixers</a>
							    	<a className="dropdown-item" href="#">Phoenix Suns</a>
							    	<a className="dropdown-item" href="#">Portland Trail Blazers</a>
							    	<a className="dropdown-item" href="#">Sacramento Kings</a>
							    	<a className="dropdown-item" href="#">San Antonio Spurs</a>
							    	<a className="dropdown-item" href="#">Toronto Raptors</a>
							    	<a className="dropdown-item" href="#">Utah Jazz</a>
							    	<a className="dropdown-item" href="#">Washington Wizards</a>
								</div>
							</div>

							<div className="dropdown mt-3">
								<button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							    	Select Year
							 	</button>
								<div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
							    	<a className="dropdown-item" href="#">2019-20</a>
							    	<a className="dropdown-item" href="#">2018-19</a>
							    	<a className="dropdown-item" href="#">2017-18</a>
							    	<a className="dropdown-item" href="#">2016-17</a>
							    	<a className="dropdown-item" href="#">2015-16</a>
							    	<a className="dropdown-item" href="#">2014-15</a>
								</div>	
							</div>


---------------------------  REFERENCE: 

Selection Menu
https://getbootstrap.com/docs/4.0/components/forms/#select-menu

<select class="custom-select">
  <option selected>Open this select menu</option>
  <option value="1">One</option>
  <option value="2">Two</option>
  <option value="3">Three</option>
</select>

Table:
https://www.w3schools.com/bootstrap4/bootstrap_tables.asp

Git pull from master to branch:
https://stackoverflow.com/questions/20101994/git-pull-from-master-into-the-development-branch
*/