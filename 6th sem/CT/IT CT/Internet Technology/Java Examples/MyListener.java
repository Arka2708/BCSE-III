

import javax.servlet.*;
import javax.servlet.ServletContextListener;
import javax.servlet.annotation.WebListener;
import java.sql.*;

/**
 * Application Lifecycle Listener implementation class MyListener
 *
 */
@WebListener
public class MyListener implements ServletContextListener {

    
	/**
     * @see ServletContextListener#contextDestroyed(ServletContextEvent)
     */
    public void contextDestroyed(ServletContextEvent sce)  { 
         // TODO Auto-generated method stub
    	ServletContext sc = sce.getServletContext();
    	try {
    		((Connection)sc.getAttribute("keyConnection")).close();
    	}catch(Exception e) {}
    }

	/**
     * @see ServletContextListener#contextInitialized(ServletContextEvent)
     */
    public void contextInitialized(ServletContextEvent sce)  { 
    	ServletContext sc = sce.getServletContext();
		String connString = sc.getInitParameter("key1");
		String connDriver=sc.getInitParameter("key1Driver");
		
		String connUser = sc.getInitParameter("key1User");
		sc.setAttribute("key3", connUser);
		
		String connPwd = sc.getInitParameter("key1Pwd");
		
		try{  
			Class.forName(connDriver);  
			Connection con=DriverManager.getConnection(connString,connUser,connPwd);  
			sc.setAttribute("keyConnection",con);
 
		}catch(Exception e){ System.out.println(e);}
    }
	
}
