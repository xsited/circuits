import org.libvirt.*;

public class minitest {
    public static void main(String[] args) {
        Connect conn=null;
        try{
            conn = new Connect("test:///default", true);
        } catch (LibvirtException e){
            System.out.println("exception caught:"+e);
            System.out.println(e.getError());
        }
        try{
            Domain testDomain=conn.domainLookupByName("test");
            System.out.println("Domain:" + testDomain.getName() + " id " +
                               testDomain.getID() + " running " +
                               testDomain.getOSType());
        } catch (LibvirtException e){
            System.out.println("exception caught:"+e);
            System.out.println(e.getError());
        }
    }
}

