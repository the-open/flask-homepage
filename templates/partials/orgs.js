var orgs = [
  {% for org in site.orgs %}
  {
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates: {{ org.coordinates }}
    },
    properties: {
      title: '{{ org.title }}',
      description: '{% if org.logo %}<img src="{{ org.logo }}" alt="{{ org.title }}" /><br />{% endif %}{{ org.description }}',
      category: '{{ org.category }}'
    }
  }{% if forloop.last %}{% else %},{% endif %}
  {% endfor %}
];
