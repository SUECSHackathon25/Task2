import Layout from '@/components/Layout/Layout'

export default async function Judges() {

    try {
      const response = await fetch('http://backend:5000/api/judges', {
        method: 'GET',
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error('Error:', error);
    }
  

 
  return (
    <Layout pageTitle={'Judges'}>

        List of judges here

      

    </Layout>
  
  )
}