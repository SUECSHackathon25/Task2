'use client';
import { UploadFile } from '@mui/icons-material'
import { yupResolver } from '@hookform/resolvers/yup'

import { Box, Button, IconButton, TextField, Typography } from '@mui/material'
import axios from 'axios';
import React from 'react'
import { Controller, Form, SubmitHandler, useForm } from 'react-hook-form'
import { InferType, mixed, object} from 'yup'


type Props = {
    title: string

}

const schema = object().shape({
    file: mixed()
        .required("A file is required")
        .test("fileFormat", "Only Excel files are allowed", (value) => {
            if (value && Array.isArray(value)) {
                return value[0]?.type === 'application/vnd.ms-excel' ||
                    value[0]?.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
            }
            return false;
        })
        .test("fileSize", "File size must be less than 5MB", (value) => {
            if (value && Array.isArray(value)) {
                return value[0]?.size <= 5 * 1024 * 1024;
            }
            return false;
        }),
})

export type FormInputs = InferType<typeof schema>;

export default function UploadExcel({ title }: Props) {


    const formSubmitHandler: SubmitHandler<FormInputs> = async (data: FormInputs) => {


        const formData = new FormData();

        console.log(data)

    }




    const { control, handleSubmit, formState: { errors } } = useForm<FormInputs>({
        resolver: yupResolver(schema),  // Make sure to use yup validation resolver
    });

    console.log(schema)
    return (
        <Box>
            <Typography variant='h2'>{title}</Typography>
            <Form control={control}>
                <Controller
                    name='file'
                    key={'file'}
                    control={control}
                    render={({ field: { value, onChange, ...field }, fieldState }) => (
                        <Box>
                            <TextField
                                {...field}
                                onChange={(event) => {
                                    // Cast the event target to HTMLInputElement
                                    const fileInput = event.target as HTMLInputElement;
                                    const file = fileInput.files ? fileInput.files[0] : null; // Get the first file
                                    onChange(file ? [file] : []);  // Pass the file as an array to react-hook-form
                                }}
                                type="file"
                                variant="outlined"
                                fullWidth
                                margin="normal"
                                error={!!fieldState?.error}
                                helperText={fieldState?.error?.message} // Display validation error
                            />
                    
                        </Box>
                    )}


                />


                <Button onClick={handleSubmit(formSubmitHandler)} >Submit</Button>

            </Form>
        </Box>



    )
}



