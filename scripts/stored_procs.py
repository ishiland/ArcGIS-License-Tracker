mssql = [
    # All users list
    '''
    CREATE PROC flexlm_all_users
    AS
    SELECT users.name,  SUM(DATEDIFF(minute, history.time_out, ISNULL(history.time_in,CURRENT_TIMESTAMP))) as time_sum,
    MAX(CASE WHEN history.time_in IS NULL AND history.time_out is NOT NULL THEN 'Y' ELSE 'N' END) AS active,
    MIN(history.time_out) as join_date
    FROM flexlm_user users
    LEFT JOIN flexlm_history history ON users.id=history.user_id
    LEFT JOIN flexlm_product products ON products.id=history.product_id
    GROUP BY users.name
    ORDER BY users.name ASC, time_sum DESC
    ''',

    # all workstations list
    '''
    CREATE PROC flexlm_all_workstations
    AS
    SELECT workstations.name,  SUM(DATEDIFF(minute, history.time_out, ISNULL(history.time_in,CURRENT_TIMESTAMP))) as time_sum,
    MAX(CASE WHEN history.time_in IS NULL AND history.time_out is NOT NULL THEN 'Y' ELSE 'N' END) AS active,
    MIN(history.time_out) as join_date
    FROM flexlm_workstation workstations
    LEFT JOIN flexlm_history history ON workstations.id=history.workstation_id
    LEFT JOIN flexlm_product products ON products.id=history.product_id
    GROUP BY workstations.name
    ORDER BY workstations.name ASC, time_sum DESC
    ''',

    # product usage history
    '''
    CREATE PROC flexlm_product_usage_history @days smallint
    AS
    SELECT Convert(char(8), history.time_out, 112) as date, count(distinct users.name) as users, products.license_total, DATENAME(weekday, history.time_out) as weekday,
    DATEPART(mm, history.time_out) as month, DATENAME(day, history.time_out) as day, DATENAME(year, history.time_out) as year
    FROM flexlm_user users
    INNER JOIN flexlm_history history ON users.id=history.user_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
    where products.common_name = 'Desktop-Advanced' and history.time_out > DATEADD(Day,-@days,getdate()) and DATENAME(weekday, history.time_out) NOT IN ('Saturday', 'Sunday')
    GROUP BY Convert(char(8), history.time_out, 112), DATENAME(weekday, history.time_out), products.license_total, DATEPART(mm, history.time_out), DATENAME(day, history.time_out),DATENAME(year, history.time_out)
    ORDER BY Convert(char(8), history.time_out, 112) ASC
    ''',

    # current active users by product and server
    '''
    CREATE PROC flexlm_active_users_by_product @productname varchar(30), @servername varchar(30)
    AS
    SELECT users.name, workstations.name as workstation, SUM(DATEDIFF(minute, history.time_out, ISNULL(history.time_in,CURRENT_TIMESTAMP))) as current_session
    FROM flexlm_user users
    INNER JOIN flexlm_history history ON users.id=history.user_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
    INNER JOIN flexlm_workstation workstations on workstations.id=history.workstation_id
    INNER JOIN flexlm_server server ON server.id=products.server_id
    where products.common_name = @productname AND server.name=@servername AND history.time_in IS NULL
    GROUP BY users.name,workstations.name,history.time_out
    ORDER BY history.time_out ASC
    ''',

    # username details
    '''
    CREATE PROC flexlm_user_usage_details @username varchar(30)
    AS
    SELECT products.common_name, server.name servername, products.type,
    SUM(DATEDIFF(minute,history.time_out, (CASE WHEN history.time_in IS NULL THEN GETDATE() ELSE history.time_in END))) as total_time,
    MAX(CASE WHEN history.time_in IS NULL THEN 'Y' ELSE 'N' END) AS in_use,
    MAX(history.time_out) as last_use
    FROM flexlm_user users
    INNER JOIN flexlm_history history ON users.id=history.user_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
    INNER JOIN flexlm_server server ON server.id=products.server_id
    where users.name = @username
    GROUP BY server.name, products.common_name, products.type, history.product_id
    ORDER BY last_use DESC
    ''',

    # user workstations
    '''
    CREATE PROC flexlm_user_workstation @username varchar(30)
    AS
    SELECT workstations.name,
    SUM(DATEDIFF(minute,history.time_out, (CASE WHEN history.time_in IS NULL THEN GETDATE() ELSE history.time_in END))) as total_time,
    MAX(CASE WHEN history.time_in IS NULL THEN 'Y' ELSE 'N' END) AS in_use,
    MAX(history.time_out) as last_use
    FROM flexlm_user users
    INNER JOIN flexlm_history history ON users.id=history.user_id
    INNER JOIN flexlm_workstation workstations ON workstations.id=history.workstation_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
    where users.name = @username and products.type ='core'
    GROUP BY workstations.name
    ORDER BY last_use DESC
    ''',

    # user server usage
    '''
    CREATE PROC flexlm_user_server @username varchar(30)
    AS
    SELECT servers.name,
    SUM(DATEDIFF(minute,history.time_out, (CASE WHEN history.time_in IS NULL THEN GETDATE() ELSE history.time_in END))) as total_time,
    MAX(CASE WHEN history.time_in IS NULL THEN 'Y' ELSE 'N' END) AS in_use,
    MAX(history.time_out) as last_use
    FROM flexlm_user users
    INNER JOIN flexlm_history history ON users.id=history.user_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
    INNER JOIN flexlm_server servers ON servers.id=products.server_id
    where users.name = @username and products.type ='core'
    GROUP BY servers.name
    ORDER BY last_use DESC
    ''',

    # workstation details
    '''
    CREATE PROC flexlm_ws_usage_details @wsname varchar(30)
    AS
    SELECT products.common_name, server.name servername, products.type,
    SUM(DATEDIFF(minute,history.time_out, (CASE WHEN history.time_in IS NULL THEN GETDATE() ELSE history.time_in END))) as total_time,
    MAX(CASE WHEN history.time_in IS NULL THEN 'Y' ELSE 'N' END) AS in_use,
    MAX(history.time_out) as last_use
    FROM flexlm_workstation workstations
    INNER JOIN flexlm_history history ON workstations.id=history.workstation_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
    INNER JOIN flexlm_server server ON server.id=products.server_id
    where workstations.name = @wsname
    GROUP BY server.name, products.common_name, products.type
    ORDER BY last_use DESC
    ''',

    # workstation users
    '''
    CREATE PROC flexlm_ws_user @wsname varchar(30)
    AS
    SELECT users.name,
    SUM(DATEDIFF(minute,history.time_out, (CASE WHEN history.time_in IS NULL THEN GETDATE() ELSE history.time_in END))) as total_time
    FROM flexlm_workstation workstations
    INNER JOIN flexlm_history history ON workstations.id=history.workstation_id
    INNER JOIN flexlm_user users ON users.id=history.user_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
    where workstations.name = @wsname and products.type ='core'
    GROUP BY users.name
    ''',

    # workstation server usage
    '''
    CREATE PROC flexlm_ws_server @wsname varchar(30)
    AS
    SELECT servers.name,
    SUM(DATEDIFF(minute,history.time_out, (CASE WHEN history.time_in IS NULL THEN GETDATE() ELSE history.time_in END))) as total_time
    FROM flexlm_workstation workstations
    INNER JOIN flexlm_history history ON workstations.id=history.workstation_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
    INNER JOIN flexlm_server servers ON servers.id=products.server_id
    where workstations.name = @wsname and products.type ='core'
    GROUP BY servers.name
    ''',

    # All products by license server
    '''
    CREATE PROC flexlm_products_by_server @producttype varchar(30), @server varchar(30)
    AS
    SELECT products.common_name, products.type, products.license_out, products.license_total
    FROM flexlm_product products
    INNER JOIN flexlm_server servers ON servers.id=products.server_id
    where products.type = @producttype AND servers.name=@server
    ''',

    # product availability
    '''
    CREATE PROC flexlm_product_availability @producttype varchar(30), @servername varchar(30)
    AS
    SELECT  products.common_name, products.license_out, products.license_total
    FROM flexlm_product products
    INNER JOIN flexlm_server servers ON products.server_id=servers.id
    where products.type = @producttype AND servers.name = @servername
    ''',

    # product info
    '''
    CREATE PROC flexlm_product_status @productname varchar(30), @servername varchar(30)
    AS
    SELECT  products.common_name, products.internal_name, products.category, products.type, products.license_out, products.license_total
    FROM flexlm_product products
    INNER JOIN flexlm_server servers ON products.server_id=servers.id
    where products.common_name = @productname AND servers.name = @servername
    ''',

    # product chart data
    '''
    CREATE PROC flexlm_product_chartdata @productName varchar(30), @sname varchar(30), @dayRange smallint
    AS
    SELECT Convert(char(8), history.time_out, 112) as date, count(distinct users.name) as users, products.license_total, DATENAME(weekday, history.time_out) as weekday,
    DATENAME(month, history.time_out) as month, DATENAME(day, history.time_out) as day
    FROM flexlm_user users
    INNER JOIN flexlm_history history ON users.id=history.user_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
    INNER JOIN flexlm_server servers ON products.server_id=servers.id
    where products.common_name = @productName and servers.name = @sname and history.time_out > DATEADD(Day,-@dayRange,getdate()) --and DATENAME(weekday, history.time_out) NOT IN ('Saturday', 'Sunday')
    GROUP BY Convert(char(8), history.time_out, 112), DATENAME(weekday, history.time_out), products.license_total, DATENAME(month, history.time_out), DATENAME(day, history.time_out)
    ORDER BY Convert(char(8), history.time_out, 112) ASC
    ''',

    # product details
    '''
    CREATE PROC flexlm_product_usage_details @pname varchar(30), @sname varchar(30)
    AS
    SELECT users.name,
    SUM(DATEDIFF(minute,history.time_out, (CASE WHEN history.time_in IS NULL THEN GETDATE() ELSE history.time_in END))) as total_time,
    MAX(CASE WHEN history.time_in IS NULL THEN 'Y' ELSE 'N' END) AS in_use,
    MAX(history.time_out) as last_check_out
    FROM flexlm_user users
    INNER JOIN flexlm_history history ON users.id=history.user_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
    INNER JOIN flexlm_server servers ON servers.id=products.server_id
    where products.common_name = @pname and servers.name = @sname
    GROUP BY users.name
    ORDER BY last_check_out DESC
    ''',

    # product workstation usage
    '''
    CREATE PROC flexlm_product_workstation @pname varchar(30), @server varchar(30)
    AS
    SELECT workstations.name,
    SUM(DATEDIFF(minute,history.time_out, (CASE WHEN history.time_in IS NULL THEN GETDATE() ELSE history.time_in END))) as total_time
    FROM flexlm_product products
    INNER JOIN flexlm_history history ON products.id=history.product_id
    INNER JOIN flexlm_workstation workstations ON workstations.id=history.workstation_id
    INNER JOIN flexlm_server servers ON products.id=products.server_id
    where products.common_name = @pname and servers.name = @server
    GROUP BY workstations.name
    ORDER BY total_time DESC
    ''',

    # list all servers
    '''
    CREATE PROC flexlm_servers_all
    AS
    select * from
    (select s.name, u.server_id, status,
    time_start,
    DATEDIFF(MS, u.time_start, u.time_complete) as total_time,
    RANK() OVER (partition by u.server_id order by u.time_start desc) as RankID
    from flexlm_server s
    inner join flexlm_update u
    on s.id=u.server_id) a
    where a.RankID=1
    ''',

    # user count of server
    '''
    CREATE PROC flexlm_server_unique_users @server varchar(30)
    AS
    SELECT count(distinct(users.name)) user_count
    FROM flexlm_user users
    LEFT JOIN flexlm_history history ON users.id=history.user_id
    LEFT JOIN flexlm_update updates ON updates.id=history.update_id
    INNER JOIN flexlm_server servers ON updates.server_id=servers.id
    where servers.name = @server
    ''',

    # server error history
    '''
    CREATE PROC flexlm_server_history @server varchar(30)
    AS
    SELECT updates.status, updates.info,
    dateadd(DAY,0, datediff(day,0, updates.time_complete)) day
    FROM flexlm_update updates
    INNER JOIN flexlm_server servers ON updates.server_id=servers.id
    where servers.name = @server and updates.status <> 'OK'
    GROUP BY updates.status, updates.info, dateadd(DAY,0, datediff(day,0, updates.time_complete))
    ORDER BY dateadd(DAY,0, datediff(day,0, updates.time_complete)) DESC
    ''',

    # server products
    '''
    CREATE PROC flexlm_server_products @server varchar(30)
    AS
    select products.common_name
    FROM flexlm_product products
    INNER JOIN flexlm_server servers ON products.server_id=servers.id
    where servers.name = @server
    ''',

    # server tracking start date
    '''
    CREATE PROC flexlm_server_startdate @server varchar(30)
    AS
    SELECT TOP 1 updates.time_start
    FROM flexlm_update updates
    INNER JOIN flexlm_server servers ON updates.server_id=servers.id
    where servers.name = @server
    ORDER BY updates.time_start ASC
    ''',

    # server status
    '''
    CREATE PROC flexlm_server_status @server varchar(30)
    AS
    SELECT TOP 1 servers.name, updates.status, updates.info, updates.time_start,
    SUM(DATEDIFF(SECOND,updates.time_start, updates.time_complete)) as total_time
    FROM flexlm_update updates
    INNER JOIN flexlm_server servers ON updates.server_id=servers.id
    where servers.name = @server
    GROUP BY servers.name, updates.status, updates.info, updates.time_start
    ORDER BY updates.time_start DESC
    ''',

    # server usage over time. For chart.
    '''
    CREATE PROC flexlm_server_usage_chart @dayrange int, @server varchar(30)
    AS 	SELECT count(distinct users.name) as users, Convert(char(8), history.time_out, 112) as d, DATENAME(weekday, history.time_out) as weekday,
    DATENAME(month, history.time_out) as month, DATENAME(day, history.time_out) as day
    FROM flexlm_user users
    INNER JOIN flexlm_history history ON users.id=history.user_id
    INNER JOIN flexlm_product products ON products.id=history.product_id
	  INNER JOIN flexlm_server servers ON servers.id=products.server_id
    WHERE products.type = 'core' and history.time_out > DATEADD(Day,-@dayrange,getdate()) and servers.name = @server
    GROUP BY Convert(char(8), history.time_out, 112), DATENAME(weekday, history.time_out), DATENAME(month, history.time_out), DATENAME(day, history.time_out)
    ORDER BY Convert(char(8), history.time_out, 112) ASC
    '''
]
