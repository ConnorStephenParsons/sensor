"""from datetime import datetime, timedelta
date_chart = pygal.Line(x_label_rotation=20)
date_chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), [
 datetime(2013, 1, 2),
 datetime(2013, 1, 12),
 datetime(2013, 2, 2),
 datetime(2013, 2, 22)])
date_chart.add("Visits", [300, 412, 823, 672])
date_chart.render()"""