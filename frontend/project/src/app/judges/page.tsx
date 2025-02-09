import Layout from '@/components/Layout/Layout'
import { Box } from '@mui/material';

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
      <Box paddingTop={'2%'}>
      List of judges here
      </Box>

      

    </Layout>
  
  )
}