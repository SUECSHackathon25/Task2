import { yupResolver } from '@hookform/resolvers/yup';
import { Box, Button, TextField, Typography } from '@mui/material';
import axios from 'axios';
import React from 'react';
import { Controller, Form, SubmitHandler, useForm } from 'react-hook-form';
import { InferType, mixed, object } from 'yup';

// Props type
type Props = {
    title: string;
    path: string;
};

// Form inputs type
type FormInputs = InferType<typeof schema>;


// Yup schema validation
const schema = object({
    file: mixed()
        .required("A file is required")
        .test("fileFormat", "Only Excel files are allowed", (value) => {
            // Ensure value is of type FileList and check file format
            if (value instanceof FileList && value.length > 0) {
                const file = value[0];
                return (
                    file.type === 'application/vnd.ms-excel' ||
                    file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                );
            }
            return false;
        })
        .test("fileSize", "File size must be less than 5MB", (value) => {
            // Ensure value is of type FileList and check file size
            if (value instanceof FileList && value.length > 0) {
                const file = value[0];
                return file.size <= 5 * 1024 * 1024;  // 5MB
            }
            return false;
        }),
});

export default function UploadExcel({ title, path }: Props) {
    const formSubmitHandler: SubmitHandler<FormInputs> = async (data: FormInputs) => {
        if (data.file) {

            if (data.file instanceof FileList) {
                const file = data.file[0];  // Get the first file from the FileList
                console.log("Uploaded file:", file);
                const formData = new FormData();
                formData.append('file', file);
        
                axios.post(path, formData)
                    .then(response => {
                        console.log(response);
                    })
                    .catch(error => {
                        console.error(error);
                    });
            } else {
                console.log("No file selected.");
            }
            }
   
    };

    const { control, handleSubmit, formState: {  } } = useForm<FormInputs>({
        resolver: yupResolver(schema), // Pass the correct resolver
    });

    return (
        <Box>
            <Typography variant='h2'>{title}</Typography>
            <Form control={control}>
                <Controller
                    name='file'
                    key={'file'}
                    control={control}
                    render={({ field: {  onChange, ...field }, fieldState }) => (
                        <Box>
                            <TextField
                                {...field}
                                onChange={(event) => {
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
                <Button onClick={handleSubmit(formSubmitHandler)}>Submit</Button>
            </Form>
        </Box>
    );
}
