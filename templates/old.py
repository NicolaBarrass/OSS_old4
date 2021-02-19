# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:30:15 2020

@author: snbar
"""

    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
 <p>{{ form.dt() }}</p>
 <p>
 <p>

<p>{{ form.select() }}</p>
</form>


 <div class="row">
 
  <div class="column5">
  <form_mon action="" method="post" novalidate>
        {{ form.hidden_tag() }}
  <h5>MONDAY</h5>
  <p>{{today[0]}}
    <p>
  {{am_list[0]}}
  {% if am_list[0]!=[] %}
      {{ form_mon.open_pat_am() }}
       {{ form_mon.cancel_am() }}
  {% else %}
      {{ form_mon.make_am() }}
   {% endif %}
  <p>
    <p>
  {{pm_list[0]}}
  {% if pm_list[0]!=[] %}
      {{ form_mon.open_pat_pm() }}
       {{ form_mon.cancel_pm() }}
  {% else %}
      {{ form_mon.make_pm() }}
   {% endif %}
  <p>
  </form_mon>
  
  </div>
  <div class="column5"><h5>TUESDAY</h5>
   <p>{{today[1]}}   <p>
  {{am_list[1]}}
  {% if am_list[1]!=[] %}
      {{ form_tue.open_pat_am() }}
       {{ form_tue.cancel_am() }}
  {% else %}
      {{ form_tue.make_am() }}
   {% endif %}
  <p>
    <p>
  {{pm_list[1]}}
  {% if pm_list[1]!=[] %}
      {{ form_tue.open_pat_pm() }}
       {{ form_tue.cancel_pm() }}
  {% else %}
      {{ form_tue.make_pm() }}
   {% endif %}
  <p>
  </div>
  <div class="column5"><h5>WEDNESDAY</h5>
   <p>{{today[2]}}   <p>
  {{am_list[2]}}
  {% if am_list[2]!=[] %}
      {{ form_wed.open_pat_am() }}
       {{ form_wed.cancel_am() }}
  {% else %}
      {{ form_wed.make_am() }}
   {% endif %}
  <p>
    <p>
  {{pm_list[2]}}
  {% if pm_list[2]!=[] %}
      {{ form_wed.open_pat_pm() }}
       {{ form_wed.cancel_pm() }}
  {% else %}
      {{ form_wed.make_pm() }}
   {% endif %}
  <p>
  </div>
  <div class="column5"><h5>THURSDAY</h5>
  <p>{{today[3]}}    <p>
  {{am_list[3]}}
  {% if am_list[3]!=[] %}
      {{ form_thu.open_pat_am() }}
       {{ form_thu.cancel_am() }}
  {% else %}
      {{ form_thu.make_am() }}
   {% endif %}
  <p>
    <p>
  {{pm_list[3]}}
  {% if pm_list[3]!=[] %}
      {{ form_thu.open_pat_pm() }}
       {{ form_thu.cancel_pm() }}
  {% else %}
      {{ form_thu.make_pm() }}
   {% endif %}
      <p>

</div>
  <div class="column5"><h5>FRIDAY</h5>
  <p>{{today[4]}}    <p>
  {{am_list[4]}}
  {% if am_list[4]!=[] %}
      {{ form_fri.open_pat_am() }}
       {{ form_fri.cancel_am() }}
  {% else %}
      {{ form_fri.make_am() }}
   {% endif %}
  <p>
    <p>
  {{pm_list[4]}}
  {% if pm_list[4]!=[] %}
      {{ form_fri.open_pat_pm() }}
       {{ form_fri.cancel_pm() }}
  {% else %}
      {{ form_fri.make_pm() }}
   {% endif %}
      <p>
  </div>
</div> 