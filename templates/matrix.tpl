<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">
<body id="matrix">
	<form action="/matrix" method="post" accept-charset="utf-8">
		
		<label for="memcache_key">MemCache Key</label><input type="text" name="memcache_key" value="" id="memcache_key" />
		<p><input type="submit" value="Continue &rarr;"></p>
	</form>
	
	
	<form action="/matrix/delete/key" method="post" accept-charset="utf-8">
		{% if key_value %}
		<p>{{key_value}}</p>
		{% else %}
		<p>wasn't found</p>
		{% endif %}
		<label for="are_your_sure_you_want_to_delete_this_key">Are your sure you want to delete this key</label><input type="text" name="del_key" value="{{key_to_delete}}" id="are_your_sure_you_want_to_delete_this_key" />
		<p><input type="submit" value="Continue &rarr;"></p>
	</form>
	
	<form action="/matrix/delete/all" method="post" accept-charset="utf-8">
		<label for="flush_all">Flush all memcache ?</label><input type="text" name="del_key" value="all" id="flush_all" />
		<p><input type="submit" value="Continue &rarr;"></p>
	</form>
</body>
</html>