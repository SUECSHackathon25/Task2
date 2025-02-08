import Layout from '@/components/Layout/Layout'
import { Box, Typography } from '@mui/material'
import UploadExcel from '@/components/Upload/UploadExcel'

export default function AdminHome() {
  return (
    <Layout pageTitle={"Admin Home Page"}>

        <Box>
            <Typography variant='h2'>Configure Judges</Typography>
            
                  
            <UploadExcel title='upload judges' path='/api/admin/judges'/>


        </Box>

    </Layout>
  
  )
}