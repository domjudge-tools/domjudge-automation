# Swagger YAML Configuration Guide

## Overview

The Swagger/OpenAPI documentation is now configured using a YAML file instead of JavaScript. This makes it easier to maintain and modify the API documentation.

## File Structure

```
backend/
├── src/
│   ├── config/
│   │   ├── swagger.yaml    # OpenAPI specification in YAML format
│   │   └── swagger.mjs     # Loads and processes the YAML file
```

## How It Works

1. **swagger.yaml**: Contains the complete OpenAPI 3.0 specification in YAML format
2. **swagger.mjs**: Loads the YAML file, parses it, and dynamically updates server URLs with the port from configuration

## Editing the Swagger Documentation

### Adding a New Endpoint

1. Open `src/config/swagger.yaml`
2. Add the endpoint definition under the `paths:` section:

```yaml
paths:
  /api/v1/your-endpoint:
    get:
      summary: Your endpoint summary
      tags:
        - YourTag
      responses:
        '200':
          description: Success response
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
```

### Adding a New Schema

1. Open `src/config/swagger.yaml`
2. Add the schema under `components/schemas:`:

```yaml
components:
  schemas:
    YourNewSchema:
      type: object
      properties:
        field1:
          type: string
        field2:
          type: number
```

### Updating Server URLs

The server URLs are automatically updated from the configuration file. To change the port, update your `.env` file:

```env
PORT=3000
```

The `swagger.mjs` file will automatically update the server URLs when the server starts.

## YAML File Structure

```yaml
openapi: 3.0.0          # OpenAPI version
info:                   # API information
  title: ...
  version: ...
  description: ...
servers:                # Server URLs (dynamically updated)
  - url: http://localhost:3000
paths:                  # API endpoints
  /api/v1/teams:
    post: ...
    get: ...
components:             # Reusable components
  schemas:              # Data models
  securitySchemes:      # Authentication schemes
tags:                   # Endpoint tags
  - name: Teams
```

## Benefits of YAML

1. **Easier to Read**: YAML is more human-readable than JavaScript objects
2. **Easier to Edit**: No need to worry about JavaScript syntax
3. **Version Control Friendly**: Changes are easier to review in Git
4. **Tool Support**: Many tools can validate and process YAML OpenAPI specs
5. **Separation of Concerns**: Documentation is separated from code

## Validation

You can validate your YAML file using online tools:
- [Swagger Editor](https://editor.swagger.io/)
- [OpenAPI Validator](https://validator.swagger.io/)

## Loading Process

1. Server starts
2. `swagger.mjs` reads `swagger.yaml`
3. YAML is parsed to JavaScript object
4. Server URLs are updated with dynamic port
5. Swagger UI is served with the processed specification

## Example: Adding Request Examples

```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/CreateTeamRequest'
      examples:
        example1:
          summary: Basic example
          value:
            team: "Team Alpha"
            uni: "University A"
        example2:
          summary: Complete example
          value:
            team: "Team Beta"
            uni: "University B"
            email: "team@example.com"
```

## Dynamic Configuration

The `swagger.mjs` file dynamically updates:
- Server URLs (from `config.server.port`)
- Can be extended to update other values from environment variables

## Troubleshooting

### YAML Syntax Errors

If you get YAML parsing errors:
1. Check indentation (YAML is sensitive to spacing)
2. Use a YAML validator
3. Check for missing colons or incorrect quotes

### Server URLs Not Updating

If server URLs don't update:
1. Check that `config.server.port` is set correctly
2. Verify the YAML file is being loaded
3. Check server logs for errors

### Changes Not Reflecting

After editing `swagger.yaml`:
1. Restart the server
2. Clear browser cache
3. Hard refresh the Swagger UI page (Ctrl+Shift+R or Cmd+Shift+R)

## Best Practices

1. **Keep YAML Valid**: Always validate your YAML before committing
2. **Use References**: Use `$ref` to reference schemas instead of duplicating
3. **Add Examples**: Always include request/response examples
4. **Descriptive Names**: Use clear, descriptive names for schemas and endpoints
5. **Version Control**: Commit YAML changes separately from code changes for easier review

## Converting from JavaScript to YAML

If you need to convert existing JavaScript Swagger definitions to YAML:

1. Copy the JavaScript object structure
2. Convert to YAML syntax:
   - Remove commas
   - Convert `:` to `: ` (with space)
   - Use proper indentation (2 spaces)
   - Convert arrays from `[]` to `-` format
3. Validate using Swagger Editor

## Resources

- [OpenAPI Specification](https://swagger.io/specification/)
- [YAML Syntax Guide](https://yaml.org/spec/1.2.2/)
- [Swagger Editor](https://editor.swagger.io/)
- [OpenAPI Examples](https://github.com/OAI/OpenAPI-Specification/tree/main/examples)

