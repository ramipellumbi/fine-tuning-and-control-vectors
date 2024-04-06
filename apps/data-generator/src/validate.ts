/* eslint-disable @typescript-eslint/no-explicit-any */
import { Static, TArray, TObject, TSchema } from "@sinclair/typebox";
import { TypeCompiler } from "@sinclair/typebox/compiler";

const SCHEMA_METADATA_KEY = Symbol("schemaMetadata");

/**
 * The `Validatable` class is a base class that provides functionality to validate
 * an instance's data against a specified schema. It is designed to be used with
 * the `createValidatableClass` function, which creates a new class with attached
 * schema validation based on the TypeBox schema provided.
 *
 * Upon instantiation, the class data is automatically validated against the schema.
 * If the data does not conform to the schema, an error is thrown.
 */
class Validatable {
  constructor(data: any) {
    Object.assign(this, data);
  }
}

/**
 * Creates a new class that extends `Validatable` with added schema validation for its instance data.
 *
 * @param schema The TypeBox schema that will be used for validation.
 * @returns A new class that extends `Validatable` and validates its instance data against the provided schema.
 */
export function createValidatableClass<T extends TObject<any> | TArray<any>>(
  schema: T,
) {
  const schemaDecorator = Schema(schema);
  const decoratedClass = schemaDecorator(Validatable);

  return decoratedClass as unknown as {
    new (data: ConstructorParametersBySchema<T>[0]): Static<T>;
  };
}

/**
 * A decorator function that attaches a TypeBox schema to a class and provides
 * validation of instance data against that schema.
 *
 * @param schema The TypeBox schema to attach to the class.
 * @returns A class decorator that will validate instance data against the provided schema.
 */
function Schema<T extends TObject<any> | TArray<any>>(schema: T) {
  return function <C extends { new (...args: any[]): Validatable }>(
    constructor: C,
  ): C & SchemaClass<T> {
    Reflect.defineMetadata(SCHEMA_METADATA_KEY, schema, constructor);

    // A utility function to validate the instance data
    function validateInstanceData(instance: any) {
      const schema = Reflect.getMetadata(SCHEMA_METADATA_KEY, constructor);

      if (!schema) throw new Error("No schema defined for this class.");

      const validator = TypeCompiler.Compile(schema);
      const validationResult = validator.Check(instance);

      if (!validationResult) {
        const errors = validator.Errors(instance);
        const errorObjects = [];

        for (const error of errors) {
          errorObjects.push({
            type: error.type,
            schema: error.schema,
            path: error.path,
            message: error.message,
            value: error.value,
          });
        }

        const messages = errorObjects.map((error) => JSON.stringify(error));

        throw new Error(`${constructor.name} error: ${messages}`);
      }
    }

    // Return a new constructor function that will validate the instance
    return class extends constructor {
      constructor(...args: any[]) {
        super(args[0]); // Assuming the constructor takes a single argument which is an object
        validateInstanceData(this);
      }
    } as any as C & SchemaClass<T>;
  };
}

// Interface for classes that can have a schema
interface SchemaClass<T extends TSchema = any> {
  new (...args: ConstructorParametersBySchema<T>): InstanceTypeBySchema<T>;
}

// A utility type to infer constructor parameters from the schema
type ConstructorParametersBySchema<T extends TSchema> =
  T extends TObject<infer P> ? [Static<TObject<P>>] : never;

// A utility type to infer the instance type from the schema
type InstanceTypeBySchema<T extends TSchema> =
  T extends TObject<infer P> ? Static<TObject<P>> : never;
