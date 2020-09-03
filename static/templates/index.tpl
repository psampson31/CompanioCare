<html>
	<head>
		<title>Test</title>
		<link rel='stylesheet' type='text/css' href='index.css'>
		% if alert:
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>		
		<script id='alert' type='text/javascript' src='alert.js'>{{alert}}</script>
		% end
	</head>
	<body>
		<h1>
			<span id='companio'>companio</span>
			<span id='care'>care</span>
		</h1>
		% if not logged_in:
			<form method='POST' action='login'>
				<fieldset>
					<legend>Please log in</legend>
					<ul>
						<li>First Name:<br> 
							<input type='text' name='first' value='{{first}}'>
						</li>
						<br>
						<li>Last Name:<br> 
							<input type='text' name='last' value='{{last}}'>
						</li>
						<br>
						<li>Email Address:<br> 
							<input type='text' name='email' value='{{email}}'>
						</li>
						<br>
					</ul>
					<input type='submit' value='Submit Form'>
				</fieldset>
			</form>
		% else:
			<p>{{first}} {{last}} has been added to the database!</p>
			<p>Email: {{email}}</p>
			<p>Other users:</p>
			<ul>
			% for first, last, email in other_users:
				<li>{{first}} {{last}} | {{email}}</li>
			% end
			</ul>
			<a href='/'>Log out</a>
		% end
	</body>
</html>
