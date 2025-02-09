'use client';
import React, { useEffect, useState } from 'react';
import { TableContainer, Table, TableHead, TableRow, TableCell, TableBody, Paper, Box, Button } from '@mui/material';
import Layout from '@/components/Layout/Layout';
import { useParams } from 'next/navigation';
import { judge } from 'types/judge';
import { score } from 'types/scores';




export default function TestTable() {
  // Define the initial values for each cell in the left column (strings)


  const initialCellValues = [
    ['Test 1', 0],
    ['Test 2', 0],
    ['Test 4', 0],
    ['Test 5', 0],
    ['Test 6', 0],
    ['', 0], // Empty string as a test case
  ];
  const { id } = useParams();

  useEffect(() => {
    async function fetchPosts() {
      const res = await fetch(`/api/judges/${id}/posters`)
      const data: judge = await res.json()
      setJudgeName(`${data.first_name} ${data.last_name}`)
      

    }
    fetchPosts()
  }, [id])


  const [judgeName, setJudgeName] = useState<string>("")
  const [cellValues, setCellValues] = useState(initialCellValues);

  // Handle button click to set ranking value
  const handleButtonClick = (rank: number, rowIndex: number) => {
    const updatedValues = [...cellValues];
    updatedValues[rowIndex][1] = rank; // Set the ranking in the right column
    setCellValues(updatedValues);
  };

  const handleSubmit = () => {
    // Placeholder for the submit function
    console.log('Form submitted with values:', cellValues);
  };

  return (
    <Layout pageTitle={`Judge Posters: ${judgeName}`}>
      <Box sx={{ margin: '0 10%' }} paddingTop={'5%'}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell></TableCell>
                <TableCell></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {cellValues.map((row, rowIndex) => (
                <TableRow key={rowIndex}>
                  <TableCell>{row[0]}</TableCell>
                  <TableCell>
                    {row[0] !== "" && ( // Only show buttons if the left-hand cell is not an empty string
                      <Box display="flex" flexWrap="wrap" justifyContent="center">
                        {/* Render buttons for selecting rank 1 to 10 in two rows */}
                        {Array.from({ length: 10 }).map((_, index) => (
                          <Button
                            key={index}
                            variant={row[1] === index + 1 ? 'contained' : 'outlined'} // Highlight the selected button
                            color="primary"
                            onClick={() => handleButtonClick(index + 1, rowIndex)} // Update rank on click
                            sx={{ margin: '4px' }} // Set width to fit buttons in two rows
                          >
                            {index + 1}
                          </Button>
                        ))}
                      </Box>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        {/* Centered Submit Button */}
        <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
          <Button variant="contained" color="primary" onClick={handleSubmit}>
            Submit All
          </Button>
        </Box>
      </Box>
    </Layout>

  )
}

