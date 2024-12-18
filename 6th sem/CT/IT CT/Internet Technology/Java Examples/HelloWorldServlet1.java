

import java.io.IOException;
import javax.servlet.*;
import javax.servlet.annotation.*;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.sql.*;

/**
 * Servlet implementation class HelloWorldServlet1
 */
@WebServlet(value={"/srvtrialversion", "/SelectCoffeeMVC.do"}, initParams = { 
		   @WebInitParam(name = "foo", value = "Hello "), 
		   @WebInitParam(name = "bar", value = " World!") 
		}) 
public class HelloWorldServlet1 extends HttpServlet {
	private static final long serialVersionUID = 1L;

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		String result="";
		CoffeeExpert ce=new CoffeeExpert();
		String color=request.getParameter("color");
		String addOn=request.getParameter("addOns");
		try{  
			
			Connection con=(Connection) getServletContext().getAttribute("keyConnection");
			result = ce.getBrands(color,addOn,con);
			//response.getWriter().append("<br>"+result);
 
		}catch(Exception e){ System.out.println(e);}
		
		request.setAttribute("results", result);
        RequestDispatcher view =
            request.getRequestDispatcher("result.jsp");
        view.forward(request, response);
	}

}
