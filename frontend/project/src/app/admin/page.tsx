import Layout from '@/components/Layout/Layout'
import { Box, Typography } from '@mui/material'
import UploadExcel from '@/components/Upload/UploadExcel'

export default function AdminHome() {
  return (
    <Layout pageTitle={'Admin Home Page'}>

        <Box>
            <Typography paddingBottom={'5%'} variant='h2'>Configure Event</Typography>
            
                  
            <UploadExcel title='Upload Judges Excel Doc' path='/api/admin/judges'/>


        </Box>

    </Layout>
  
  )
}