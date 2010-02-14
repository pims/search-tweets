{% include 'head.tpl' %}
<body id="home">
{% include 'top.tpl' %}
	
	{% if error %}
		<div class="error full box">{{error}}</div>
	{% else %}
		<section id="results">
			{% if results %}				
				{% for result in results %}
				<div class="single-result full box"><p>{{result.text}}</p><span>tweeted by <a href="http://twitter.com/{{result.user}}/statuses/{{result.id}}">{{result.user}}</a> and favorited by @{{result.favorited_by|join:", @"}}</span></div>
				{% endfor %}
			{% else %}
				<div class="error full box">Oops ! We haven’t found what you’re looking for. <a href="http://www.djangoproject.com/">Oh look, a pony !</a></div>
			{% endif %}
		</section>	
	{% endif %}
{% include 'footer.tpl'%}
<script src="/static/js/app.js" type="text/javascript" charset="utf-8"></script>
{{analytics}}
</body>
</html>